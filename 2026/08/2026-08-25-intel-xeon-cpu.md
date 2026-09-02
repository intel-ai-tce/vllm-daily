# Intel Xeon and CPU-Related Merged PRs

**Report Date:** 2026-08-25 PDT

**Source:** [vLLM Merged PR Report for 2026-08-25](./2026-08-25.md)

No merged PR in the source report explicitly mentions Intel Xeon. The entries below are the CPU- or host-memory-related PRs: they affect CPU container builds, host-resident KV-cache behavior, or observability for host-to-device cache traffic. XPU- and GPU-only changes are excluded.

| PR | Title | CPU/host relevance | Source section |
| --- | --- | --- | --- |
| [#51335](https://github.com/vllm-project/vllm/pull/51335) | [5/N] Expose HiSparse cache metrics | Adds host-cache hit/miss and host-to-device byte metrics for HiSparse. | [Section 15](./2026-08-25.md#15-5n-expose-hisparse-cache-metrics) |
| [#51323](https://github.com/vllm-project/vllm/pull/51323) | [4/N] HiSparse: host-resident sparse-MLA decode hot-buffering | Introduces host-resident KV-cache storage and touches the CPU model runner as part of the host/GPU offload path. | [Section 16](./2026-08-25.md#16-4n-hisparse-host-resident-sparse-mla-decode-hot-buffering) |
| [#53290](https://github.com/vllm-project/vllm/pull/53290) | [CI] Preserve Rust Docker cache across commits | Updates `docker/Dockerfile.cpu` and improves caching for CPU image builds. | [Section 22](./2026-08-25.md#22-ci-preserve-rust-docker-cache-across-commits) |

## Open Xeon and CPU-Related Issues

**Snapshot date:** 2026-09-01 PDT

This snapshot includes open vLLM issues whose titles mention CPU, Xeon, NUMA, or a CPU-specific x86 feature. It excludes GPU-only issues where `x86_64` is only a CUDA wheel platform and where the title explicitly states that CPU offload is not involved. Because issue state changes over time, follow the links for current status.

| Issue | Summary | Labels | Updated (UTC) |
| --- | --- | --- | --- |
| [#16722](https://github.com/vllm-project/vllm/issues/16722) | Offload and reload vLLM weights between CPU and GPU | `usage`, `unstale` | 2026-07-22 |
| [#21231](https://github.com/vllm-project/vllm/issues/21231) | 100% CPU usage on three cores with Ray distributed pipeline parallelism | `bug`, `ray`, `unstale` | 2026-07-28 |
| [#23096](https://github.com/vllm-project/vllm/issues/23096) | Add pre-built CPU-only wheels for basic testing | `feature request`, `unstale` | 2026-07-12 |
| [#27222](https://github.com/vllm-project/vllm/issues/27222) | Reduce high CPU overhead for Qwen3-Next | `performance`, `stale` | 2026-08-26 |
| [#28467](https://github.com/vllm-project/vllm/issues/28467) | Persistent CPU RAM growth and container restarts with Qwen2-2B on SageMaker | `bug`, `unstale` | 2026-07-02 |
| [#29134](https://github.com/vllm-project/vllm/issues/29134) | Make `seq_lens_cpu` optional for fully asynchronous speculative decoding | `performance`, `unstale` | 2026-08-18 |
| [#32653](https://github.com/vllm-project/vllm/issues/32653) | CPU offload still results in out-of-VRAM errors | `usage` | 2026-07-15 |
| [#36796](https://github.com/vllm-project/vllm/issues/36796) | CPU offload errors on NVIDIA GH200 unified memory | `bug`, `torch.compile` | 2026-06-18 |
| [#38515](https://github.com/vllm-project/vllm/issues/38515) | vLLM crash while using CPU offloading | `bug` | 2026-08-06 |
| [#39427](https://github.com/vllm-project/vllm/issues/39427) | SubSpec speculative decoding for CPU-offloaded LLMs | `feature request`, `unstale` | 2026-07-29 |
| [#41437](https://github.com/vllm-project/vllm/issues/41437) | macOS ARM64 CPU attention vector build regression | `cpu` | 2026-07-18 |
| [#41615](https://github.com/vllm-project/vllm/issues/41615) | Polymorphic CPU/GPU staged-buffer management for the V1 worker | `feature request`, `stale` | 2026-08-04 |
| [#42207](https://github.com/vllm-project/vllm/issues/42207) | Clear CPU-resident memory left by unloaded LoRA adapters | `usage`, `stale` | 2026-08-14 |
| [#42348](https://github.com/vllm-project/vllm/issues/42348) | Gemma 4 KV-cache CPU offloading is broken | `bug` | 2026-08-10 |
| [#42371](https://github.com/vllm-project/vllm/issues/42371) | SimpleCPUOffloadConnector requests get stuck under sustained load | `bug` | 2026-07-15 |
| [#43240](https://github.com/vllm-project/vllm/issues/43240) | Performance drop across NUMA nodes in `ompmultiprocessing.py` | `bug`, `stale`, `cpu` | 2026-08-27 |
| [#43326](https://github.com/vllm-project/vllm/issues/43326) | GELU_TANH unsupported in the CPU fused-MoE path for Gemma 4 | `bug` | 2026-07-06 |
| [#43563](https://github.com/vllm-project/vllm/issues/43563) | Intel Xeon prefill/decode disaggregation | `usage`, `stale` | 2026-08-24 |
| [#43775](https://github.com/vllm-project/vllm/issues/43775) | Replace hard-coded Granite Rapids PCT detection with a generic root-free NUMA path | `feature request`, `keep-open` | 2026-05-27 |
| [#44200](https://github.com/vllm-project/vllm/issues/44200) | Qwen3-VL video pruning CPU/CUDA device mismatch | `stale` | 2026-08-31 |
| [#44341](https://github.com/vllm-project/vllm/issues/44341) | Slow ROCm simple CPU offload without batched mapping | `rocm`, `stale` | 2026-09-01 |
| [#44354](https://github.com/vllm-project/vllm/issues/44354) | AMD Zen CPU CI | `feature request`, `rocm` | 2026-08-18 |
| [#44421](https://github.com/vllm-project/vllm/issues/44421) | RFC for AMD Zen CPU CI infrastructure | `rocm`, `RFC` | 2026-06-04 |
| [#44867](https://github.com/vllm-project/vllm/issues/44867) | Support macOS x86 in the CPU backend | `feature request`, `cpu` | 2026-06-08 |
| [#46268](https://github.com/vllm-project/vllm/issues/46268) | ModelOpt NVFP4 checkpoint causes a fixed 52 GiB CPU RAM allocation | — | 2026-08-26 |
| [#46470](https://github.com/vllm-project/vllm/issues/46470) | InternLM2 embedding-layer regression on the CPU backend | `bug`, `cpu` | 2026-06-23 |
| [#46693](https://github.com/vllm-project/vllm/issues/46693) | Qwen3.5 CPU backend crashes when Triton is unavailable | `cpu` | 2026-06-25 |
| [#47014](https://github.com/vllm-project/vllm/issues/47014) | Dynamic speculative decoding crashes on the CPU backend | `cpu` | 2026-08-29 |
| [#47328](https://github.com/vllm-project/vllm/issues/47328) | CPU data-parallel affinity regression | `bug` | 2026-09-01 |
| [#48277](https://github.com/vllm-project/vllm/issues/48277) | Plugin registration failures silently cause CPU fallback | — | 2026-07-10 |
| [#48919](https://github.com/vllm-project/vllm/issues/48919) | CPU offloading fails with block size 256 and speculative decoding | `bug` | 2026-07-20 |
| [#49122](https://github.com/vllm-project/vllm/issues/49122) | Aria tensor-parallel output corruption reproducible on CPU | `bug` | 2026-07-21 |
| [#49210](https://github.com/vllm-project/vllm/issues/49210) | Engine-core livelock with 100% CPU usage under MTP and xgrammar | `structured-output` | 2026-08-31 |
| [#49460](https://github.com/vllm-project/vllm/issues/49460) | Grammar thread pool is host-CPU-count and cgroup unaware | `structured-output` | 2026-08-31 |
| [#50821](https://github.com/vllm-project/vllm/issues/50821) | Native CPU offload computes inconsistent block counts across PP ranks | `bug` | 2026-08-03 |
| [#51080](https://github.com/vllm-project/vllm/issues/51080) | CPU offload cannot pin regions of 512 GiB or more | — | 2026-08-04 |
| [#51283](https://github.com/vllm-project/vllm/issues/51283) | Structured outputs crash the CPU backend | `bug`, `structured-output`, `cpu` | 2026-08-31 |
| [#51396](https://github.com/vllm-project/vllm/issues/51396) | `cpu_offload_gb` silently no-ops with Model Runner V2 | — | 2026-08-08 |
| [#51533](https://github.com/vllm-project/vllm/issues/51533) | Worker CPU deadloop after NCCL initialization | `installation` | 2026-08-09 |
| [#52008](https://github.com/vllm-project/vllm/issues/52008) | Kimi K3 cannot run on CPU due to an MLA/Mamba prefix-cache conflict | `bug`, `kimi`, `k3` | 2026-08-12 |
| [#52025](https://github.com/vllm-project/vllm/issues/52025) | Rust frontend template evaluation can consume 55 CPU-seconds per request | `bug` | 2026-08-12 |
| [#52238](https://github.com/vllm-project/vllm/issues/52238) | CPU platform silently falls back when zentorch import fails | `bug` | 2026-08-20 |
| [#52407](https://github.com/vllm-project/vllm/issues/52407) | NVFP4 emulation crashes from a CPU/GPU lookup-table device mismatch | `bug`, `quantization` | 2026-08-15 |
| [#52583](https://github.com/vllm-project/vllm/issues/52583) | CPU-bound hash alignment blocks multimodal prefix-cache prefill | `bug` | 2026-08-29 |
| [#52656](https://github.com/vllm-project/vllm/issues/52656) | OffloadingConnector crashes above 64 GB of CPU RAM | `bug`, `rocm` | 2026-08-18 |
| [#52916](https://github.com/vllm-project/vllm/issues/52916) | Bounded x86 WAITPKG and ARM WFET waits for shared-memory broadcast | `cpu` | 2026-08-19 |
| [#53368](https://github.com/vllm-project/vllm/issues/53368) | Expose CPU-versus-P2P attribution for multi-tier KV restores | — | 2026-08-24 |
| [#53607](https://github.com/vllm-project/vllm/issues/53607) | CPU KV offload crashes on DeepSeek-V4 MLA cache layouts | `deepseek`, `DSv4` | 2026-08-24 |
| [#53931](https://github.com/vllm-project/vllm/issues/53931) | `--cpu-offload-params` cannot reach token embeddings outside `make_layers` | `quantization` | 2026-08-29 |
| [#53960](https://github.com/vllm-project/vllm/issues/53960) | PLE CPU offload deadlocks during single-GPU kernel warmup | `quantization` | 2026-09-01 |
| [#54018](https://github.com/vllm-project/vllm/issues/54018) | GLM-5.x cannot run on CPU because sparse attention cannot be disabled | `glm` | 2026-08-27 |
| [#54415](https://github.com/vllm-project/vllm/issues/54415) | Shared-mmap CPU region hangs multi-node KV-offload engines | — | 2026-08-30 |
| [#54504](https://github.com/vllm-project/vllm/issues/54504) | Nemotron-H prefix caching crashes on the CPU backend | `cpu`, `kv-cache-manager` | 2026-09-01 |
| [#54593](https://github.com/vllm-project/vllm/issues/54593) | `--cpu-offload-gb` evicts hot MoE weights first | — | 2026-08-31 |
| [#54843](https://github.com/vllm-project/vllm/issues/54843) | FP64 Gumbel option is ignored in CPU recovered-token sampling | — | 2026-09-02 |
