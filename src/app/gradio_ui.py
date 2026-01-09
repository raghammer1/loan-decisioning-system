import gradio as gr
from app.llm.client import generate

SYSTEM_PROMPT = (
    "You are a helpful assistant for a credit/loan decisioning project. "
    "Be concise, explain assumptions, and ask clarifying questions when needed."
)

def ensure_history(history):
    return history if isinstance(history, list) else []

def history_to_prompt(history):
    lines = [SYSTEM_PROMPT]
    for m in history[-5:]:
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


    if not user_input or not user_input.strip():
        return history, history

    # 1) Add user message to history
    history.append({"role": "user", "content": user_input})

    # 2) Create the prompt you actually send to the model
    # (For now we’re using a simple combined prompt. Later we can send structured messages.)
    prompt = history_to_prompt(history)

    # 3) Call the model safely
    try:
        response = generate(prompt)
    except Exception as e:
        response = f"⚠️ Error calling LLM: {type(e).__name__}: {e}"

    # 4) Add assistant message to history
    history.append({"role": "assistant", "content": response})

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
