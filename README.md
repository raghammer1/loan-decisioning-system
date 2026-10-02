# Loan explanation prototype

A learning project exploring explanations of sample loan outcomes. The repository contains an LLM explanation layer and an **incomplete decision-engine scaffold**. It is not a completed underwriting engine or a production service.

## Implementation status

| Area | Current source state |
| --- | --- |
| Explanation layer | Gemini client, tool routing, CSV record lookup, prompt construction and Gradio chat code are present. They require configuration and compatible dependencies. |
| HTTP API | `/health` and `/ask` routes exist. `/ask` currently calls `generate` with one argument although its implementation requires two; this path needs repair before use. |
| Decision pipeline | Eligibility, verification, bureau, servicing and decision modules are scaffolded. Several modules, policy-rule files and call wrappers are empty. |
| Tests and CI | No checked-in test suite or CI workflow was found on the reviewed branch. A pytest configuration is not a passing test suite. |
| ML and persistence | Design documents discuss ML scoring, DuckDB and Parquet. A working end-to-end implementation has not been established. |

## Source map

- `src/app/gradio_ui.py`: chat interface and history-to-prompt assembly.
- `src/app/llm/client.py`: Gemini calls and tool enrichment.
- `src/app/llm/tools/`: tool dispatch and sample application-record lookup.
- `src/decisioning/`: incomplete decision and policy scaffold.
- `data/`: sample CSV files, not evidence of real lending outcomes.
- `docs/`: design intentions and project notes; see the status table above before treating a document as implemented behavior.

The explanation path reads sample records and constructs a model prompt. It does not establish a complete decision pipeline. This project is separate from any employer system and must not be used to make real lending decisions.

## Local development prerequisites

Python 3.11 or later. `pyproject.toml` declares core dependencies but does not currently declare all imports used by the UI and model layer (`gradio` and `google-genai`). The wheel configuration includes `src/decisioning`, not the `app` package. Resolve these packaging gaps before treating installation as reproducible.

The intended source-tree entry points are documented in [how to run](docs/how_to_run.md). Gemini use requires your own `GEMINI_API_KEY` and may incur provider charges. No model calls are required to read or inspect this repository. Do not put credentials, real customer records or employer policies into the source or prompts.

## Next engineering steps

1. Repair the HTTP call contract and declare the complete runtime dependencies.
2. Implement one deterministic vertical slice with explicit inputs, outcomes and reason codes.
3. Add unit and integration tests for that slice, plus missing-record and provider-failure cases.
4. Add CI, then update documentation using actual test and benchmark results.

No performance, fairness, compliance or production-readiness result is claimed.
