import streamlit as st
from groq import Groq

def build_messages(system_prompt, chat_history):
    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        if msg.get("role") in ["user", "assistant"] and isinstance(msg.get("content"), str):
            messages.append({
                "role": msg["role"],
                "content": msg["content"][:2000]
            })
    return messages

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Organ Donation Chatbot",
    layout="centered"
)

# -------------------- LOAD API KEY --------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -------------------- LOAD PROJECT KNOWLEDGE --------------------
with open("project_knowledge.txt", "r") as file:
    project_info = file.read()

# -------------------- UI HEADER --------------------
st.title("AI-Powered Organ Donation Assistant")
st.caption("24×7 Intelligent Support for Donors, Recipients & Administrators")

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- DISPLAY CHAT HISTORY --------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- USER INPUT --------------------
user_input = st.chat_input("Ask your question about organ donation...")

if user_input:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------- AI RESPONSE --------------------
    with st.spinner("Thinking..."):

        try:
    messages = build_messages(system_prompt, st.session_state.messages)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.3,
        max_tokens=500
    )

    bot_reply = response.choices[0].message.content

except Exception:
    bot_reply = "⚠️ Sorry, the AI service is temporarily unavailable. Please try again."

    # Store assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
