### To run the LLM Agent:
Run the FastAPI Server : uv run uvicorn app.main:app --reload --app-dir src

### To run the Gradio App:
Run : PYTHONPATH=src uv run python src/app/gradio_ui.py