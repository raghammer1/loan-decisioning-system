# Local development status

The project is incomplete. These are intended source-tree entry points, not a verified clean-install quick start.

Python 3.11+ is required. Core dependencies are in `pyproject.toml`, but `google-genai` and `gradio` imports are not yet declared there. The wheel includes `decisioning`, not `app`.

After resolving those dependency gaps in an isolated environment:

```sh
PYTHONPATH=src python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
PYTHONPATH=src python src/app/gradio_ui.py
```

The `/health` route exists. The `/ask` route needs a call-signature fix before use: it passes one argument to a function requiring `prompt` and `user_input`. The Gradio path passes both arguments but has not been validated end to end in this documentation pass.

The current LLM client uses Gemini, not Ollama. It expects your own `GEMINI_API_KEY`; `GEMINI_MODEL` and `LLM_PROVIDER` are read from the environment. Provider requests may be billable. Do not use customer data. There is no checked-in automated test suite or CI workflow.
