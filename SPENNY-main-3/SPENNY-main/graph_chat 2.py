# graph_chat.py  (inside graph-ui)

import os, traceback, gradio as gr, pytesseract
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- core helpers -----------------------------------------------------------
def ocr_image(img: Image.Image) -> str:
    """Return OCR text (or '' if img is None)."""
    if img is None:
        return ""
    return pytesseract.image_to_string(img, lang="eng")


def gpt_reply(messages):
    """Call GPT-4o-mini with current history & return assistant reply."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=400,
    )
    return resp.choices[0].message.content


# --- Gradio event handlers ---------------------------------------------------
def handle_upload(img, chat_history):
    """
    Called when user uploads a screenshot *or* types a prompt.
    img: PIL or None (Gradio passes None when user only types text)
    chat_history: list[(user, assistant)] for Chatbot display
    """
    try:
        # Convert chat_history -> messages list
        messages = [{"role": "system",
                     "content": ("You are a concise, insightful trading-graph analyst. "
                                 "When user asks for stop-loss or entry, give clear "
                                 "price levels based on chart context.")}]
        for user_msg, bot_msg in chat_history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})

        if img is not None:
            # 1️⃣  run OCR
            ocr_text = ocr_image(img)
            user_msg = f"Here is the chart text:\n\n{ocr_text}"
        else:
            # When only text typed, latest input is already last item in chat_history
            user_msg = chat_history[-1][0]

        # Append the (possibly OCR) user message to history
        messages.append({"role": "user", "content": user_msg})

        # 2️⃣  GPT insight
        assistant_msg = gpt_reply(messages)

        # 3️⃣  Update chat_history for display in Chatbot
        chat_history[-1] = (user_msg, assistant_msg)
        return chat_history, gr.update(value=None), ""      # reset error box

    except Exception as e:
        tb = traceback.format_exc()
        return chat_history, gr.update(value=None), f"❌ {e}\n{tb[-500:]}"


def add_user_text(user_txt, chat_history):
    """Push user’s typed prompt into chat_history then wait for handle_upload."""
    if user_txt.strip() == "":
        return chat_history
    chat_history.append((user_txt, ""))   # assistant will be filled next step
    return chat_history


# --- Build Gradio UI ---------------------------------------------------------
with gr.Blocks(title="📈  Graph → GPT Chat") as demo:
    gr.Markdown("### 1) Drag a chart screenshot  **or**  just type a question\n"
                "Then keep chatting for stop-loss, R-R, etc.")

    with gr.Row():
        img_in = gr.Image(type="pil", label="Screenshot (optional)")
        error_box = gr.Markdown("", elem_id="err", show_label=False)

    chatbot = gr.Chatbot(label="Conversation", height=400)

    txt_in = gr.Textbox(
        label="Your message (Enter to send)",
        placeholder="Ask follow-ups like: Where should I place my stop?"
    )

    # Events
    txt_in.submit(add_user_text,        [txt_in, chatbot], chatbot
    ).then(handle_upload,               [img_in, chatbot], [chatbot, img_in, error_box])

    img_in.upload(
        lambda img, chat: (chat + [("Uploaded chart", "")], ),
        [img_in, chatbot], chatbot
    ).then(handle_upload,               [img_in, chatbot], [chatbot, img_in, error_box])

if __name__ == "__main__":
    demo.launch()

