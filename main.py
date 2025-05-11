import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

st.set_page_config(page_title="Simple Chat App", page_icon="💬")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = pd.DataFrame(columns=["timestamp", "user", "message"])

st.title("💬 Simple Chat App")

# User input
user = st.text_input("👤 Enter your name:", key="user_input")

# Generate a new key every time a message is sent to reset input field
if "message_key" not in st.session_state:
    st.session_state.message_key = str(uuid.uuid4())  # Initialize a new unique key

# Create a unique key for the message input to force new UI every time
message = st.text_input("💬 Type your message:", key=st.session_state.message_key)

# Function to identify coding-related questions and give answers
def ai_response(user_msg):
    user_msg = user_msg.lower().strip()
    
    # Greetings
    if "hi" in user_msg or "hello" in user_msg:
        return "Hey there! 👋 How can I help you today? 😊"
    
    # How are you?
    elif "how are you" in user_msg or "how do you do" in user_msg:
        return "I'm just a bot, but I'm doing great! 😄 What about you? 🌟"
    
    # Bye message
    elif "bye" in user_msg:
        return "Goodbye! 👋 Have a great day ahead! 🌞"
    
    # Help message
    elif "help" in user_msg:
        return "Sure! 🤖 I'm here to assist you. What do you need help with? 💡"
    
    # Coding-related question
    elif "code" in user_msg or "python" in user_msg or "programming" in user_msg:
        return (
            "It looks like you're asking about coding! 🖥️ Here's a simple Python example:\n\n"
            "```python\n"
            "def greet(name):\n"
            "    return f'Hello, {name}!'\n\n"
            "name = input('Enter your name: ')\n"
            "print(greet(name))\n"
            "```"
            "\nThis is a basic Python function to greet someone. You can modify it and try it out!"
        )
    
    # Ask what the bot is doing
    elif "what are you doing" in user_msg:
        return "Waiting for your next message! ⏳ What do you want to talk about? 🗣️"
    
    # A generic response if no match
    elif "thank you" in user_msg or "thanks" in user_msg:
        return "You're welcome! 😊 Happy to help! 💙"
    
    else:
        return f"You said: *{user_msg}*... That’s interesting! 😲 Let’s talk more! 🗣️"

# Send message
if st.button("📤 Send"):
    if user and message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_msg = pd.DataFrame([{
            "timestamp": timestamp,
            "user": user,
            "message": message
        }])
        st.session_state.messages = pd.concat([st.session_state.messages, new_msg], ignore_index=True)

        # AI response
        ai_msg = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": "AI Bot",
            "message": ai_response(message)
        }])
        st.session_state.messages = pd.concat([st.session_state.messages, ai_msg], ignore_index=True)

        # Update the message_key to force a new input box (reset)
        st.session_state.message_key = str(uuid.uuid4())
        st.rerun()

# Clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.messages = pd.DataFrame(columns=["timestamp", "user", "message"])
    st.rerun()

# Download chat
if not st.session_state.messages.empty:
    st.download_button(
        label="📥 Download Chat History",
        data=st.session_state.messages.to_csv(index=False),
        file_name="chat_history.csv",
        mime="text/csv"
    )

# Display chat history
st.subheader("🕘 Chat History")
for _, row in st.session_state.messages.iterrows():
    with st.chat_message(row["user"]):
        st.markdown(f"**[{row['timestamp']}] {row['user']}**: {row['message']}")
