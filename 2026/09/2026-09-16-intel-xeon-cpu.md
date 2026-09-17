# Intel Xeon and CPU-Related Upstream Update

**Report date:** 2026-09-16 PDT

**Repositories:** [`vllm-project/vllm`](https://github.com/vllm-project/vllm) and [`vllm-project/recipes`](https://github.com/vllm-project/recipes)

**Baseline:** [Open Xeon and CPU-related issues as of 2026-09-01](../08/2026-08-25-intel-xeon-cpu.md#open-xeon-and-cpu-related-issues)

This report covers merged changes and newly opened issues since the baseline. Direct Intel Xeon, x86 CPU-backend, and architecture-neutral CPU-backend work is listed first. Host-memory and CPU-offload work that can affect Xeon hosts is kept in a separate section because it is not specific to Xeon execution. ARM-only, AMD-only, Intel XPU/GPU-only, and generic GPU issues are excluded.

## Merged changes

### `vllm-project/vllm`

| PR | Merged | Summary | Xeon/CPU relevance |
| --- | --- | --- | --- |
| [#55355](https://github.com/vllm-project/vllm/pull/55355) | 2026-09-10 | Add DeepSeek-V4 CPU backend | Adds the DeepSeek-V4 CPU model path and CPU kernels for sparse MLA, routing, MoE, MHC, cache handling, and related operations, together with CPU hardware tests. |
| [#56773](https://github.com/vllm-project/vllm/pull/56773) | 2026-09-14 | Fix DeepSeek-R1 (FP8 MLA + MoE) correctness on CPU backend | Corrects scaled-matrix-multiplication and fused-MoE behavior for DeepSeek-R1 on CPU. |
| [#56671](https://github.com/vllm-project/vllm/pull/56671) | 2026-09-14 | Mock CPU backend block sizes in KV-connector unit tests | Makes KV-connector unit tests model CPU-backend block-size behavior explicitly. This is test-only but protects CPU compatibility. |

### `vllm-project/recipes`

| PR | Merged | Summary | Xeon/CPU relevance |
| --- | --- | --- | --- |
| [#961](https://github.com/vllm-project/recipes/pull/961) | 2026-09-16 | Add missing Docker commands to CPU recipes | Updates 26 model recipes with corrected or completed Xeon CPU Docker guidance, including Gemma, Qwen, Llama, Phi, GPT-OSS, Whisper, and GLM recipes. |

## New open `vllm-project/vllm` issues

### Direct CPU-backend and x86 relevance

| Issue | Opened | Summary | Labels |
| --- | --- | --- | --- |
| [#54843](https://github.com/vllm-project/vllm/issues/54843) | 2026-09-01 | FP64 Gumbel is ignored in CPU recovered-token sampling. | — |
| [#55005](https://github.com/vllm-project/vllm/issues/55005) | 2026-09-02 | The CPU speculative-decoding `expand_kernel` shim discards its output, leaving sampling inputs uninitialized. | — |
| [#55560](https://github.com/vllm-project/vllm/issues/55560) | 2026-09-06 | The CPU MoE kernel can produce NaN logits under `torch.compile` for Qwen3.5 MoE models. | `torch.compile`, `quantization` |
| [#55613](https://github.com/vllm-project/vllm/issues/55613) | 2026-09-06 | AWQ/GPTQ WNA16 int4 GEMM is unavailable on AVX2-only CPUs because there is no non-AVX-512 fallback. | `quantization` |
| [#55614](https://github.com/vllm-project/vllm/issues/55614) | 2026-09-06 | Logs and opt-in Prometheus metric names incorrectly hard-code “GPU” on CPU and other non-GPU backends. | — |
| [#56419](https://github.com/vllm-project/vllm/issues/56419) | 2026-09-11 | CPU Gated-DeltaNet with MTP and structured output can crash the engine or silently corrupt output. | `structured-output`, `speculative-decoding`, `tool-calling` |

### Host CPU and CPU-offload relevance

| Issue | Opened | Summary | Labels |
| --- | --- | --- | --- |
| [#55503](https://github.com/vllm-project/vllm/issues/55503) | 2026-09-05 | Multi-tier CPU/filesystem KV offload with MTP can crash `EngineCore`. | `speculative-decoding`, `quantization` |
| [#56283](https://github.com/vllm-project/vllm/issues/56283) | 2026-09-10 | `--cpu-offload-gb` can select `NoopOffloader`, leaving weights on the accelerator. | `bug`, `quantization` |
| [#56410](https://github.com/vllm-project/vllm/issues/56410) | 2026-09-11 | `--cpu-offload-gb` can consume about 1.9 times the requested host memory. | `bug` |
| [#56507](https://github.com/vllm-project/vllm/issues/56507) | 2026-09-11 | The EC CPU connector documentation references a no-NIXL import test that does not exist. | `kv-connector` |
| [#56871](https://github.com/vllm-project/vllm/issues/56871) | 2026-09-14 | CPU KV-offload capacity is divided incorrectly across cache groups on hybrid models. | — |

## Xeon recipe changes and issues

The following upstream `vllm` changes and issues may require new or revised Xeon recipes. These are recipe-impact candidates, not a status list; each recommended action should be validated on Xeon before changing a recipe.

| Upstream item | Priority | Xeon recipe impact | Candidate recipe change |
| --- | --- | --- | --- |
| [PR #55355](https://github.com/vllm-project/vllm/pull/55355) — DeepSeek-V4 CPU backend | High | The existing `deepseek-ai/DeepSeek-V4-Pro` recipe has GPU entries but no Xeon hardware declaration or CPU launch path. The new CPU backend makes a Xeon recipe path possible. | Validate a supported DeepSeek-V4 checkpoint on Xeon, then add `xeon6` hardware metadata, CPU image/install instructions, topology guidance, and CPU-safe feature defaults. |
| [PR #56773](https://github.com/vllm-project/vllm/pull/56773) — DeepSeek-R1 FP8 MLA + MoE CPU correctness fix | High | The existing `deepseek-ai/DeepSeek-R1` recipe does not advertise Xeon, although the merged fix specifically targets its CPU execution path. | Validate DeepSeek-R1 on Xeon with a build containing #56773. If successful, add Xeon hardware/topology and Docker guidance and set the minimum vLLM version to the first release containing the fix. |
| [Issue #55005](https://github.com/vllm-project/vllm/issues/55005) — CPU speculative-decoding sampling corruption | High | Non-greedy speculative decoding may be incorrect on CPU. Xeon-enabled recipes exposing speculative decoding include Qwen3.5, Gemma 4, and Llama 3.1 recipes. | Until fixed and validated, suppress speculative-decoding options for `xeon6` or add an explicit CPU limitation warning. Re-enable them only with a minimum-version guard for the fix. |
| [Issue #55560](https://github.com/vllm-project/vllm/issues/55560) — Qwen3.5 MoE NaNs under `torch.compile` on CPU | High | `Qwen/Qwen3.5-35B-A3B` is marked verified on Xeon 6 and is directly exposed to this MoE correctness issue. | Revalidate the Xeon configuration; add a temporary Xeon `--enforce-eager` override or known-issue warning if it avoids the failure, then remove the workaround after an upstream fix is released. |
| [Issue #56419](https://github.com/vllm-project/vllm/issues/56419) — CPU Gated-DeltaNet + MTP structured-output failures | High | Both Xeon-enabled Qwen3.5 recipes (`Qwen3.5-4B` and `Qwen3.5-35B-A3B`) use Gated-DeltaNet and expose MTP speculative decoding. | Disable or warn against the MTP-plus-structured-output combination on Xeon, and add a regression-validation note before restoring the combination. |
| [Issue #55613](https://github.com/vllm-project/vllm/issues/55613) — WNA16 int4 unavailable on AVX2-only CPUs | Conditional | Current Xeon 5/6 recipe targets provide AVX-512, so existing recipes do not need a workaround. This becomes relevant if recipes expand to older AVX2-only Xeon systems. | If older Xeon generations are added, document the ISA requirement and exclude AWQ/GPTQ WNA16 int4 variants where the required kernel is unavailable. |

Merged recipes PR [#961](https://github.com/vllm-project/recipes/pull/961) remains the concrete Xeon recipe change in this window: it adds or corrects CPU Docker commands across 26 recipes. The table above identifies the next likely recipe work created by `vllm` runtime changes and defects.

## Snapshot notes

- Issue state and labels were checked on 2026-09-16; follow each link for current status.
- The `vllm` issue list is incremental from the 2026-09-01 baseline rather than a duplicate of the earlier full snapshot.
- “Xeon-related” includes architecture-neutral vLLM CPU-backend defects because they apply to supported Intel x86 CPU deployments. CPU offload is listed separately to distinguish host-memory behavior from native CPU inference.
