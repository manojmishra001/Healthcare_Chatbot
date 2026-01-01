import streamlit as st
from openai import OpenAI

# Initialize OpenAI client (reads from OPENAI_API_KEY env variable)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = (
    "You are a helpful assistant and expert in health related queries. "
    "Apart from health, if anything is asked, just reply: "
    "'Sorry, I can help you with health related questions only.'"
)

st.set_page_config(page_title="Health Chatbot", page_icon="🩺")
st.title("🩺 Health Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history (skip system message)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# User input
user_input = st.chat_input("Ask a health-related question...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    # Call OpenAI
    response = client.responses.create(
        model="gpt-5.2",
        input=st.session_state.messages
    )

    bot_reply = response.output_text

    # Save and show assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
    with st.chat_message("assistant"):
        st.write(bot_reply)
