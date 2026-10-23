#!/usr/bin/env python3
"""Collect cumulative vLLM distribution counters without failing on source errors.

The default collection uses Docker Hub and GitHub Releases only. PyPI's public
BigQuery dataset is strictly opt-in because it needs Google Cloud credentials,
an optional dependency, and may incur query charges.
"""

import argparse
import csv
import datetime as dt
import json
import os
from pathlib import Path
import sys
import tempfile

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("ERROR: requests is required: pip install requests", file=sys.stderr)
    raise SystemExit(2)


RELEASES_URL = "https://api.github.com/repos/vllm-project/vllm/releases"
FIELDS = ["timestamp_utc", "source", "metric", "label", "count", "notes"]


def http_session():
    retry = Retry(
        total=4,
        connect=4,
        read=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update(
        {"User-Agent": "vllm-release-download-tracker/1", "Accept": "application/json"}
    )
    return session


def fetch_json(session, url, headers=None):
    response = session.get(url, headers=headers, timeout=(10, 40))
    response.raise_for_status()
    return response.json()


def cpu_arch(filename):
    """Return the host architecture for an official +cpu wheel, else None."""
    name = filename.lower()
    if not name.endswith(".whl"):
        return None
    parts = name.split("-")
    # A wheel name is distribution-version-...-platform. Require +cpu in the
    # version component, rather than accepting a generic "cpu" substring.
    if len(parts) < 5 or "+cpu" not in parts[1]:
        return None
    platform_tag = parts[-1][:-4]
    if "x86_64" in platform_tag:
        return "x86_64"
    if "aarch64" in platform_tag or "arm64" in platform_tag:
        return "aarch64"
    return "other"


def collect_docker(session, add, errors):
    for repository in ("vllm-openai-cpu", "vllm-openai"):
        try:
            obj = fetch_json(
                session, f"https://hub.docker.com/v2/repositories/vllm/{repository}/"
            )
            add(
                "docker_hub",
                "total_pulls",
                repository,
                int(obj["pull_count"]),
                "Repository-wide cumulative pulls; may include nightly/non-release tags",
            )
        except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
            errors.append(f"Docker Hub {repository}: {type(exc).__name__}: {exc}")


def collect_github(session, add, errors, max_pages):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    totals = {"x86_64": 0, "aarch64": 0, "other": 0}
    assets = []
    complete = False
    try:
        for page in range(1, max_pages + 1):
            releases = fetch_json(
                session, f"{RELEASES_URL}?per_page=100&page={page}", headers
            )
            if not isinstance(releases, list):
                raise ValueError("unexpected GitHub response; possibly rate-limited")
            for release in releases:
                if release.get("draft") or release.get("prerelease"):
                    continue
                for asset in release.get("assets", []):
                    arch = cpu_arch(asset.get("name", ""))
                    if arch is None:
                        continue
                    downloads = int(asset["download_count"])
                    assets.append(
                        (release.get("tag_name", "?"), asset["name"], downloads, arch)
                    )
                    totals[arch] += downloads
            if len(releases) < 100:
                complete = True
                break
        if not complete:
            errors.append(
                f"GitHub Releases: pagination limit ({max_pages} pages) reached; "
                "discarded incomplete batch and published no GitHub totals"
            )
            return
        for version, name, downloads, arch in assets:
            add(
                "github_releases",
                "wheel_downloads",
                f"{version} / {name}",
                downloads,
                f"Official published non-prerelease +cpu wheel; host architecture={arch}",
            )
        for arch, downloads in totals.items():
            add(
                "github_releases",
                "wheel_downloads_total",
                arch,
                downloads,
                "All fetched published non-prerelease GitHub release +cpu wheel assets",
            )
    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        errors.append(
            f"GitHub Releases: {type(exc).__name__}: {exc}; discarded incomplete batch"
        )


def collect_pypi_bigquery(add, errors, project, max_bytes_gb):
    try:
        from google.cloud import bigquery
    except ImportError:
        errors.append(
            "PyPI BigQuery: optional google-cloud-bigquery dependency is not installed"
        )
        return
    query = """
        SELECT CASE
          WHEN REGEXP_CONTAINS(file.filename, r"(?i)_x86_64\\.whl$") THEN 'x86_64'
          WHEN REGEXP_CONTAINS(file.filename, r"(?i)_(aarch64|arm64)\\.whl$") THEN 'aarch64'
          ELSE 'other' END AS host_architecture,
          COUNT(*) AS downloads
        FROM `bigquery-public-data.pypi.file_downloads`
        WHERE file.project = 'vllm' AND ENDS_WITH(LOWER(file.filename), '.whl')
          AND timestamp < TIMESTAMP(CURRENT_DATE())
        GROUP BY host_architecture
    """
    try:
        client = bigquery.Client(project=project or None)
        dry = client.query(
            query,
            job_config=bigquery.QueryJobConfig(dry_run=True, use_query_cache=False),
        )
        max_bytes = int(max_bytes_gb * 1024**3)
        if (dry.total_bytes_processed or 0) > max_bytes:
            errors.append(
                "PyPI BigQuery skipped: estimated scan exceeds configured byte limit"
            )
            return
        result = client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                maximum_bytes_billed=max_bytes, use_query_cache=True
            ),
        ).result(timeout=240)
        totals = {row.host_architecture: int(row.downloads) for row in result}
        for arch in ("x86_64", "aarch64", "other"):
            add(
                "pypi",
                "standard_wheel_downloads_total",
                arch,
                totals.get(arch, 0),
                "Standard vLLM wheel host architecture; not CPU-only inference or GPU use",
            )
    except Exception as exc:  # SDK auth, billing and timeout exceptions vary.
        errors.append(f"PyPI BigQuery: {type(exc).__name__}: {exc}")


def read_csv(path):
    if not path.exists() or not path.stat().st_size:
        return []
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"CSV header mismatch at {path}")
        return list(reader)


def atomic_write_csv(path, existing, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    combined = existing + rows
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, suffix=".tmp", delete=False, encoding="utf-8", newline=""
        ) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(combined)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def metric_key(row):
    return (row["source"], row["metric"], row["label"])


def read_previous_latest(path):
    try:
        with path.open(encoding="utf-8") as stream:
            data = json.load(stream)
        return data.get("metrics", []) if isinstance(data, dict) else []
    except (OSError, ValueError, TypeError):
        return []


def atomic_write_latest(path, timestamp, fresh_rows, errors):
    previous = read_previous_latest(path)
    fresh_keys = {metric_key(row) for row in fresh_rows}
    metrics = [dict(row, stale=False) for row in fresh_rows]
    for row in previous:
        if metric_key(row) not in fresh_keys:
            preserved = {key: row[key] for key in FIELDS if key in row}
            if len(preserved) == len(FIELDS):
                preserved["stale"] = True
                metrics.append(preserved)
    payload = {
        "collection_timestamp_utc": timestamp,
        "status": "complete" if not errors else "partial",
        "warning_count": len(errors),
        "warnings": errors,
        "metrics": metrics,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, suffix=".tmp", delete=False, encoding="utf-8"
        ) as stream:
            temporary = Path(stream.name)
            json.dump(payload, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="data/vllm-downloads")
    parser.add_argument("--max-pages", type=int, default=100)
    parser.add_argument("--ecr-cpu", type=int, default=None)
    parser.add_argument("--ecr-arm64", type=int, default=None)
    parser.add_argument("--pypi-bigquery", action="store_true")
    parser.add_argument("--gcp-project")
    parser.add_argument("--pypi-max-gb", type=float, default=100)
    args = parser.parse_args(argv)
    if args.max_pages < 1 or args.pypi_max_gb <= 0:
        parser.error("page and BigQuery limits must be positive")
    if any(value is not None and value < 0 for value in (args.ecr_cpu, args.ecr_arm64)):
        parser.error("manual ECR counters cannot be negative")
    return args


def run(args, session=None, now=None):
    timestamp = (now or dt.datetime.now(dt.timezone.utc)).isoformat(timespec="seconds")
    rows, errors = [], []

    def add(source, metric, label, count, notes=""):
        rows.append(
            dict(
                timestamp_utc=timestamp,
                source=source,
                metric=metric,
                label=label,
                count=int(count),
                notes=notes,
            )
        )

    session = session or http_session()
    collect_docker(session, add, errors)
    for repository, count in (
        ("vllm-cpu-release-repo", args.ecr_cpu),
        ("vllm-arm64-cpu-release-repo", args.ecr_arm64),
    ):
        if count is not None:
            add(
                "ecr_public",
                "manual_total_downloads",
                repository,
                count,
                "Optional manually supplied cumulative counter",
            )
    collect_github(session, add, errors, args.max_pages)
    if args.pypi_bigquery:
        collect_pypi_bigquery(add, errors, args.gcp_project, args.pypi_max_gb)

    folder = Path(args.out)
    csv_path = folder / "vllm_download_history.csv"
    latest_path = folder / "latest.json"
    try:
        existing = read_csv(csv_path)
        if rows:
            atomic_write_csv(csv_path, existing, rows)
        atomic_write_latest(latest_path, timestamp, rows, errors)
    except (OSError, ValueError, csv.Error) as exc:
        print(f"ERROR: could not persist output: {exc}", file=sys.stderr)
        return 1

    print(f"Captured {len(rows)} fresh metrics with {len(errors)} warning(s)")
    for row in rows:
        if row["metric"] != "wheel_downloads":
            print(f"{row['source']:16} {row['label']:28} {row['count']:>13,}")
    for warning in errors:
        print(f"WARNING: {warning}", file=sys.stderr)
    return 0


def main(argv=None):
    return run(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
