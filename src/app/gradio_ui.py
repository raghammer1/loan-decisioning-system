import gradio as gr
import logging
from app.llm.client import generate
from app.globals import curr_dir
from app.logging_config import init_session_logging


init_session_logging("gradio_ui")
logger = logging.getLogger(__name__)


PROMPT_PATH = curr_dir / "llm" / "prompts" / "prompt.txt"
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")


def ensure_history(history):
    return history if isinstance(history, list) else []

def history_to_prompt(history):
    lines = [SYSTEM_PROMPT]
    for m in history:
        role = m.get("role", "")
        content = m.get("content", "")
        if role == "user":
            lines.append(f"User: {content}")
        elif role == "assistant":
            lines.append(f"Assistant: {content}")
    lines.append("Assistant:")  # cue the next response
    return "\n".join(lines)


def chat_fn(user_input, history):
    history = ensure_history(history)
    logger.info("Gradio chat_fn called user_input_len=%d", len(user_input or ""))


    if not user_input or not user_input.strip():
        logger.info("Empty user input; returning without LLM call")
        return history, history

    # 1) Add user message to history
    history.append({"role": "user", "content": user_input})
    logger.debug("History updated user_messages=%d", len(history))

    # 2) Create the prompt you actually send to the model
    # (For now we’re using a simple combined prompt. Later we can send structured messages.)
    prompt = history_to_prompt(history)
    logger.debug("Prompt built prompt_len=%d", len(prompt))

    # 3) Call the model safely
    try:
        response = generate(prompt, user_input)
    except Exception as e:
        logger.exception("LLM call failed")
        response = f"⚠️ Error calling LLM: {type(e).__name__}: {e}"

    # 4) Add assistant message to history
    history.append({"role": "assistant", "content": response})
    logger.debug("Assistant response appended response_len=%d", len(response or ""))

    return history, history


with gr.Blocks(title="Decisioning LLM") as demo:
    gr.Markdown("## 🧠 Decisioning LLM Chat (Correct Messages Format)")

    chatbot = gr.Chatbot(height=420)
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(placeholder="Ask a question...", scale=4, show_label=False)
        send = gr.Button("Send", scale=1)

    send.click(chat_fn, inputs=[txt, state], outputs=[chatbot, state])
    txt.submit(chat_fn, inputs=[txt, state], outputs=[chatbot, state])

    clear = gr.Button("Clear")
    clear.click(lambda: ([], []), outputs=[chatbot, state])

demo.launch()
