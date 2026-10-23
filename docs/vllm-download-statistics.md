# vLLM download statistics

The daily workflow records cumulative distribution counters at 09:15 UTC and can
also be run from **Actions → Collect vLLM download statistics → Run workflow**.

The default run needs only Python, `requests`, and the repository-provided
`GITHUB_TOKEN`. It collects repository-wide Docker Hub pull counters for
`vllm/vllm-openai-cpu` and `vllm/vllm-openai`, plus download counters for official
published, non-prerelease `+cpu` wheel assets from `vllm-project/vllm` releases.
CPU wheel totals are grouped by x86-64, ARM64, and other host architectures.

Docker Hub exposes a repository-wide cumulative pull count, so these values can
include nightly and other non-release tags. All metrics are download or pull
events—not unique users, installations, deployments, or hardware utilization.
The standard `vllm-openai` image is kept separate from CPU inference distribution.

AWS ECR counters are optional manual CLI inputs (`--ecr-cpu` and `--ecr-arm64`).
PyPI BigQuery collection is completely disabled by default. Enabling it requires
`--pypi-bigquery`, Google authentication, and `google-cloud-bigquery`; its wheel
architecture is the host architecture and does not imply CPU-only inference or
actual GPU use.

History is appended atomically to
`data/vllm-downloads/vllm_download_history.csv`; the most recent state is written
atomically to `data/vllm-downloads/latest.json`. A failed source does not stop
healthy sources. Its previous latest metrics are retained with `"stale": true`,
and warnings make the partial collection explicit. An incomplete GitHub pagination
batch is discarded rather than reported as an all-time total.

The workflow needs **Actions → General → Workflow permissions → Read and write
permissions** and permission for GitHub Actions to create pull requests. It first
attempts to commit to `main`. If branch protection rejects that push, it updates
the persistent `automation/vllm-download-statistics-data` branch and opens or
updates a pull request without weakening protection. Run artifacts are retained
for 30 days as an additional recovery and inspection aid.
