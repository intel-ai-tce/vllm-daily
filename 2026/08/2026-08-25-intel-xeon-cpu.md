# Intel Xeon and CPU-Related Merged PRs

**Report Date:** 2026-08-25 PDT

**Source:** [vLLM Merged PR Report for 2026-08-25](./2026-08-25.md)

No merged PR in the source report explicitly mentions Intel Xeon. The entries below are the CPU- or host-memory-related PRs: they affect CPU container builds, host-resident KV-cache behavior, or observability for host-to-device cache traffic. XPU- and GPU-only changes are excluded.

| PR | Title | CPU/host relevance | Source section |
| --- | --- | --- | --- |
| [#51335](https://github.com/vllm-project/vllm/pull/51335) | [5/N] Expose HiSparse cache metrics | Adds host-cache hit/miss and host-to-device byte metrics for HiSparse. | [Section 15](./2026-08-25.md#15-5n-expose-hisparse-cache-metrics) |
| [#51323](https://github.com/vllm-project/vllm/pull/51323) | [4/N] HiSparse: host-resident sparse-MLA decode hot-buffering | Introduces host-resident KV-cache storage and touches the CPU model runner as part of the host/GPU offload path. | [Section 16](./2026-08-25.md#16-4n-hisparse-host-resident-sparse-mla-decode-hot-buffering) |
| [#53290](https://github.com/vllm-project/vllm/pull/53290) | [CI] Preserve Rust Docker cache across commits | Updates `docker/Dockerfile.cpu` and improves caching for CPU image builds. | [Section 22](./2026-08-25.md#22-ci-preserve-rust-docker-cache-across-commits) |
