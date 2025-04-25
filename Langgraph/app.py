import streamlit as st
from chatbot import graph_invoke

# Page config
st.set_page_config(page_title="Simple Chatbot", page_icon="💬", layout="centered")

# CSS for clean UI
st.markdown("""
    <style>
        .stChatMessage {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 16px;
            color: #000000;
        }
        .user {
            background-color: #e0f7fa;
            text-align: right;
        }
        .bot {
            background-color: #f1f8e9;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Simple Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(f'<div class="stChatMessage {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="user_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get bot response
    response = graph_invoke(user_input)

    

    # Save bot response
    st.session_state.messages.append({"role": "bot", "content": response})

    # Rerun to update UI
    st.rerun()
