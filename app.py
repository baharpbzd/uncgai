import streamlit as st
import pandas as pd
import datetime
import os
import requests

# Set page configuration
st.set_page_config(page_title="AI Prompt Engineering", layout="wide")

# Background image from UNCG
image_url = "https://uncgcdn.blob.core.windows.net/wallpaper/Wallpaper_Minerva-UNCG_desktop_3840x2160.jpg"

# CSS customization for background and fonts
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

def generate_response(api_key, prompt):
    """Generates a response using Hugging Face Inference API."""
    api_url = "https://api-inference.huggingface.co/models/google/flan-t5-small"  # Updated model

    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}  # Correct payload structure

    try:
        # Make API request
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # Extract generated text
        result = response.json()
        generated_text = result[0].get("generated_text", "").strip()
        return generated_text
    except Exception as e:
        raise RuntimeError(f"Failed to generate response: {str(e)}")

def save_interaction(student_name, prompt, ai_response):
    """Saves the interaction to a CSV file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = pd.DataFrame(
        [[student_name, prompt, ai_response, timestamp]],
        columns=["Student", "Prompt", "AI_Response", "Timestamp"]
    )
    file_exists = os.path.isfile("student_interactions.csv")
    data.to_csv("student_interactions.csv", mode="a", header=not file_exists, index=False)

# Streamlit UI setup
st.title("AI Prompt Engineering Assignment")

# Input fields for student name, API key, and prompt
student_name = st.text_input("Enter your name:")
api_key = st.text_input("Enter your Hugging Face API Key:", type="password")
prompt = st.text_area("Write your prompt:")

# Generate AI response on button click
if st.button("Generate AI Response"):
    if student_name and api_key and prompt:
        try:
            ai_response = generate_response(api_key, prompt)
            st.subheader("AI Response")
            st.write(ai_response)

            # Save the interaction
            save_interaction(student_name, prompt, ai_response)
            st.success("Your interaction has been saved!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please provide your name, API key, and a prompt.")
