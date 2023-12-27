import streamlit as st
from openai import OpenAI
import time

st.title("Welcome to fttlzyx's chatbot powered by GPT  ᕕ(´◔⌓◔)ᕗ")

# Set OpenAI API key from Streamlit secrets (file location: ~/.streamlit/secrets.toml)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set OpenAI gpt-3.5-turbo as the model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat histroy from the memory of streamlit page
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your question here. "): 
    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt}) 

    # Display user message in chat history container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant message in chat history container
    with st.chat_message("assistant"):
        # Create a container to store ai messages
        message_placeholder = st.empty()
        full_response = ""
        # Chat Completions API from OpenAI
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True):
            full_response += (response.choices[0].delta.content or "")
            # Simulate stream of response with milliseconds delay
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add ai message to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})