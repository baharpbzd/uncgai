import openai
import streamlit as st
import pandas as pd
import datetime
import os

# Set page configuration
st.set_page_config(page_title="AI Education App", layout="wide")

# Using your image link from UNCG
image_url = "https://uncgcdn.blob.core.windows.net/wallpaper/Wallpaper_Minerva-UNCG_desktop_3840x2160.jpg"

# CSS for background and fonts
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("{image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}

h1, h2, h3, h4, h5, h6, p, div {{
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    font-size: 18px;
    color: black;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Chatbot function using OpenAI API
def chatbot_response(api_key, user_message):
    """Generates a chatbot response using OpenAI."""
    openai.api_key = api_key

    messages = st.session_state.chat_history + [{"role": "user", "content": user_message}]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Switch to "gpt-4" if needed
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response.choices[0].message["content"].strip()
        return bot_reply
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar Chatbot UI
with st.sidebar:
    st.title("Chat with AI")

    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    user_message = st.text_input("You:", value=st.session_state.user_input, key="user_input")

    if st.button("Send"):
        if api_key and user_message:
            bot_reply = chatbot_response(api_key, user_message)

            # Update chat history with user and bot messages
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

            # Clear the input field after sending
            st.session_state.user_input = ""
            st.experimental_set_query_params()  # Refresh UI to reflect updates

    # Display chat history
    if st.session_state.chat_history:
        st.write("### Chat History")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**AI:** {message['content']}")

# Function for the Prompt Engineering Page
def prompt_engineering_page():
    st.title("Prompt Engineering")
    st.write("This page is dedicated to teaching students about Prompt Engineering.")
    
    api_key = st.text_input("Enter your OpenAI API Key:", type="password", key="prompt_api_key")
    prompt = st.text_area("Write a prompt to generate an AI response:")

    if st.button("Generate AI Response", key="generate_prompt"):
        if api_key and prompt:
            try:
                response = generate_response(api_key, prompt)
                st.subheader("AI Response")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please provide both the API key and a prompt.")

# Function for the Ethics in AI Page
def ethics_in_ai_page():
    st.title("Ethics in AI")
    st.write("This page covers the ethical considerations when building and using AI systems.")
    
    st.subheader("Watch the Ethics in AI Video")
    st.video("https://youtu.be/muLPOvIEtaw?si=VkX-Vma888dwDkDA")

    st.subheader("Key Ethical Topics")
    st.write("""
    - **Bias in AI**: How algorithms can perpetuate societal biases.
    - **Transparency**: The need for clear communication on how AI makes decisions.
    - **Privacy**: Protecting user data and ensuring AI systems respect privacy.
    - **Accountability**: Defining who is responsible for the decisions made by AI systems.
    """)

# Generate AI Response using OpenAI API
def generate_response(api_key, prompt):
    """Generates a response using OpenAI's API."""
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can switch to "gpt-4" if needed
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

# Multi-Page Navigation with Sidebar
page = st.sidebar.selectbox("Select a Page", ["Prompt Engineering", "Ethics in AI"])

# Render the selected page
if page == "Prompt Engineering":
    prompt_engineering_page()
elif page == "Ethics in AI":
    ethics_in_ai_page()
