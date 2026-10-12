from pathlib import Path
import yaml
import streamlit as st
from dotenv import load_dotenv
from bot.llm import ask_gemini

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
with open(ROOT / "config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f) or {}

st.set_page_config(page_title="ClassMate", page_icon="📚", layout="wide")
st.title("📚 ClassMate")
st.caption("English for Productivity Schedule Assistant · Your friendly class and study companion")

with st.sidebar:
    st.header("⚙️ Settings")
    user_name = st.text_input("Your name", value="Student")
    class_group = st.text_input("Class group (optional)", value="")
    language = st.radio("Reply language", ["Bilingual", "English only"], index=0)
    st.selectbox("Gemini model", [CONFIG.get("model", "gemini-3.8-flash")], index=0, disabled=True)
    temperature = st.slider("Temperature", 0.0, 1.0, float(CONFIG.get("temperature", 0.2)), 0.1)
    max_tokens = st.slider("Max output tokens", 100, 1000, int(CONFIG.get("max_output_tokens", 500)), 50)
    st.caption("Model is fixed in config.yaml. Keep your API key in .env; never share it.")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": f"Hello! I’m ClassMate, your study and English productivity assistant. Ask me about homework, study planning, English practice, or productivity tips. 😊"
    }]

cols = st.columns(4)
shortcuts = [
    ("Next class", "Help me prepare a checklist for my next class."),
    ("Study plan", "Create a realistic study plan for this week."),
    ("Homework", "Help me break a homework assignment into small steps."),
    ("English practice", "Give me a short English speaking practice activity."),
]
for col, (label, value) in zip(cols, shortcuts):
    if col.button(label, use_container_width=True):
        st.session_state.pending_prompt = value

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about classes, deadlines, assignments, or study habits…")
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("ClassMate is thinking…"):
            try:
                answer = ask_gemini(
                    messages=st.session_state.messages,
                    user_name=user_name.strip() or "Student",
                    class_group=class_group.strip(),
                    language=language,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    model=CONFIG.get("model", "gemini-3.8-flash"),
                )
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as exc:
                st.error("Gemini could not complete the request.")
                st.code(str(exc)[:1200])
                st.info("Check model availability, API key permissions, connection, and quota. Never share your API key.")
