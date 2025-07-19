import streamlit as st
import requests

# Backend API URL (make sure FastAPI is running)
API_URL = "https://mychatapp.azurewebsites.net/chat"


st.set_page_config(page_title="LangChain Chatbot", page_icon="🤖")
st.title("🤖 Chat with LangChain Bot")

# Initialize chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Ask me anything...")

# If user submits a message
if user_input:
    # Show user message in UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to FastAPI
    try:
        response = requests.post(API_URL, json={"message": user_input})
        if response.status_code == 200:
            bot_reply = response.json()["response"]
        else:
            bot_reply = f"Error: {response.text}"
    except Exception as e:
        bot_reply = f"Request failed: {e}"

    # Show bot response in UI
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
