import argparse
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import requests


SCRIPT = Path(__file__).parents[1] / "scripts" / "collect_vllm_downloads.py"
SPEC = importlib.util.spec_from_file_location("collector", SCRIPT)
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


class FakeSession:
    def __init__(self, payloads):
        self.payloads = iter(payloads)

    def get(self, *args, **kwargs):
        value = next(self.payloads)
        if isinstance(value, Exception):
            raise value
        response = mock.Mock()
        response.json.return_value = value
        response.raise_for_status.return_value = None
        return response


class CollectorTests(unittest.TestCase):
    def test_cpu_wheel_classification(self):
        self.assertEqual(collector.cpu_arch("vllm-0.9.0+cpu-cp312-abi3-manylinux_x86_64.whl"), "x86_64")
        self.assertEqual(collector.cpu_arch("vllm-0.9.0+cpu-cp312-abi3-manylinux_aarch64.whl"), "aarch64")
        self.assertEqual(collector.cpu_arch("vllm-0.9.0+cpu-cp312-abi3-win_amd64.whl"), "other")
        self.assertIsNone(collector.cpu_arch("vllm-0.9.0-cp312-abi3-manylinux_x86_64.whl"))
        self.assertIsNone(collector.cpu_arch("vllm_cpu_plugin-1.0-cp312-abi3-manylinux_x86_64.whl"))

    def test_incomplete_pagination_publishes_no_github_rows(self):
        release = {"draft": False, "prerelease": False, "assets": []}
        session = FakeSession([[release] * 100])
        rows, errors = [], []
        collector.collect_github(session, lambda *args: rows.append(args), errors, 1)
        self.assertEqual(rows, [])
        self.assertIn("pagination limit", errors[0])

    def test_github_429_discards_batch(self):
        rows, errors = [], []
        collector.collect_github(
            FakeSession([requests.HTTPError("429 Too Many Requests")]),
            lambda *args: rows.append(args), errors, 5,
        )
        self.assertEqual(rows, [])
        self.assertIn("discarded incomplete batch", errors[0])

    def test_one_docker_failure_keeps_other_repository(self):
        rows, errors = [], []
        collector.collect_docker(
            FakeSession([requests.Timeout("slow"), {"pull_count": 42}]),
            lambda *args: rows.append(args), errors,
        )
        self.assertEqual(rows[0][2], "vllm-openai")
        self.assertEqual(rows[0][3], 42)
        self.assertEqual(len(errors), 1)

    def test_csv_schema_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.csv"
            path.write_text("wrong,header\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "header mismatch"):
                collector.read_csv(path)

    def test_empty_collection_preserves_csv_and_marks_latest_stale(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            row = dict(zip(collector.FIELDS, ["old", "docker_hub", "total_pulls", "vllm-openai", 9, "note"]))
            collector.atomic_write_csv(folder / "vllm_download_history.csv", [], [row])
            collector.atomic_write_latest(folder / "latest.json", "old", [row], [])
            args = argparse.Namespace(out=directory, max_pages=1, ecr_cpu=None, ecr_arm64=None,
                                      pypi_bigquery=False, gcp_project=None, pypi_max_gb=100)
            status = collector.run(args, FakeSession([
                requests.Timeout(), requests.Timeout(), requests.Timeout()
            ]))
            self.assertEqual(status, 0)
            with (folder / "vllm_download_history.csv").open() as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), 1)
            latest = json.loads((folder / "latest.json").read_text())
            self.assertTrue(latest["metrics"][0]["stale"])
            self.assertEqual(latest["status"], "partial")

    def test_missing_optional_bigquery_is_nonfatal(self):
        errors = []
        with mock.patch.dict("sys.modules", {"google": None}):
            collector.collect_pypi_bigquery(lambda *args: None, errors, None, 1)
        self.assertIn("optional", errors[0])

    def test_markdown_report_has_summary_and_methodology(self):
        row = dict(zip(collector.FIELDS, [
            "2026-10-23T09:15:00+00:00", "docker_hub", "total_pulls",
            "vllm-openai-cpu", 1234, "repository counter",
        ]))
        report = collector.render_markdown_report(
            "2026-10-23T09:15:00+00:00", [dict(row, stale=False)], []
        )
        self.assertIn(
            "| docker_hub | total_pulls | vllm-openai-cpu | 1,234 | current run |", report
        )
        self.assertIn("## How these statistics are gathered", report)
        self.assertIn("nightly and non-release tags", report)
        self.assertIn("not unique users", report)


if __name__ == "__main__":
    unittest.main()
