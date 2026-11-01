# vLLM download statistics

Collected at **2026-11-01T16:04:01+00:00**.

Status: **complete** (0 warnings).

## Cumulative totals

| Source | Metric | Distribution / architecture | Count | Freshness |
| --- | --- | --- | ---: | --- |
| docker_hub | total_pulls | vllm-openai-cpu | 502,744 | current run |
| docker_hub | total_pulls | vllm-openai | 41,909,251 | current run |
| github_releases | wheel_downloads_total | x86_64 | 428,559 | current run |
| github_releases | wheel_downloads_total | aarch64 | 91,505 | current run |
| github_releases | wheel_downloads_total | other | 0 | current run |

## Previous monthly activity

Period: **2026-10-23 to 2026-11-01** (partial baseline period).

| Source | Metric | Distribution / architecture | Events during period |
| --- | --- | --- | ---: |
| docker_hub | total_pulls | vllm-openai | 1,293,239 |
| docker_hub | total_pulls | vllm-openai-cpu | 46,605 |
| github_releases | wheel_downloads_total | aarch64 | 7,754 |
| github_releases | wheel_downloads_total | other | 0 |
| github_releases | wheel_downloads_total | x86_64 | 35,638 |

Monthly activity is the difference between cumulative counters at successive month-boundary snapshots; it is not reconstructed from current totals.

## Warnings

No collection warnings.

## How these statistics are gathered

- **Docker Hub CPU inference:** the collector reads the repository-wide cumulative `pull_count` for `vllm/vllm-openai-cpu` from the Docker Hub API.
- **Docker Hub overall/GPU-oriented distribution:** it separately reads the repository-wide cumulative `pull_count` for `vllm/vllm-openai`.
- **GitHub CPU wheels:** it paginates every release from `vllm-project/vllm`, keeps published non-draft, non-prerelease wheel assets whose version contains `+cpu`, and sums each asset's `download_count` into x86-64, ARM64, or other.
- **AWS ECR:** CPU image counters are included only when manually supplied with `--ecr-cpu` or `--ecr-arm64`; the collector never invents a value.
- **PyPI:** disabled by default. The optional BigQuery mode counts standard vLLM wheel downloads by host architecture, not CPU-only inference or actual GPU use.

## Interpretation and reliability

Counts are cumulative pull/download events, not unique users, installations, running deployments, or hardware utilization. Docker Hub's repository counter can include nightly and non-release tags. If GitHub pagination is incomplete, the entire GitHub batch is discarded rather than reporting a misleading total. When an individual source fails, its previous successful value is retained and marked as stale while healthy sources are still recorded.

Detailed per-wheel observations are available in `latest.json`; time-series history is stored in `vllm_download_history.csv`.
