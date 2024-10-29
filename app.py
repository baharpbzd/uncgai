import os
import openai
import streamlit as st
import pandas as pd
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt):
    # Generate a response using OpenAI's new client-based structure
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4"
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

# Streamlit UI setup
st.title("AI Prompt Engineering Assignment")

student_name = st.text_input("Enter your name:")
prompt = st.text_area("Write your prompt:")

if st.button("Generate AI Response"):
    if student_name and prompt:
        ai_response = generate_response(prompt)
        st.subheader("AI Response")
        st.write(ai_response)
        
        # Save the interaction (you can expand this logic)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = pd.DataFrame([[student_name, prompt, ai_response, timestamp]],
                            columns=["Student", "Prompt", "AI_Response", "Timestamp"])
        data.to_csv("student_interactions.csv", mode="a", header=False, index=False)
        st.success("Your interaction has been saved!")
    else:
        st.error("Please provide both your name and a prompt.")
