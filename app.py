import openai
import streamlit as st
import pandas as pd
import datetime
import os

# Set page configuration
st.set_page_config(page_title="AI Prompt Engineering", layout="wide")

# Using your image link from UNCG
image_url = "https://uc.uncg.edu/wp-content/uploads/2023/05/UNCG_uao_VCBG-01.png"

# CSS to set the background image
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("{image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

def generate_response(api_key, prompt):
    """Generates a response using OpenAI's API."""
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
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
api_key = st.text_input("Enter your OpenAI API Key:", type="password")  # Masked input
prompt = st.text_area("Write your prompt:")

if st.button("Generate AI Response"):
    if student_name and api_key and prompt:
        try:
            ai_response = generate_response(api_key, prompt)
            st.subheader("AI Response")
            st.write(ai_response)

            save_interaction(student_name, prompt, ai_response)
            st.success("Your interaction has been saved!")
        except Exception as e:
            st.error(str(e))
    else:
        st.error("Please provide your name, API key, and a prompt.")
