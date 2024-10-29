pip install openai==0.28 
import streamlit as st
import pandas as pd
import openai
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load existing data if available
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_interactions.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Student", "Prompt", "AI_Response", "Timestamp", "Score"])

# Save interactions to CSV
def save_interaction(student_name, prompt, ai_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = pd.DataFrame([[student_name, prompt, ai_response, timestamp, None]],
                        columns=["Student", "Prompt", "AI_Response", "Timestamp", "Score"])
    data.to_csv("student_interactions.csv", mode="a", header=False, index=False)

# Function to interact with OpenAI's GPT-3.5 model
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or "gpt-4" if available
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit UI
st.title("AI Prompt Engineering Assignment")

# Input fields
student_name = st.text_input("Enter your name:")
prompt = st.text_area("Write your prompt:")

if st.button("Generate AI Response"):
    if student_name and prompt:
        # Get AI response
        ai_response = generate_response(prompt)
        st.subheader("AI Response")
        st.write(ai_response)
        
        # Save interaction
        save_interaction(student_name, prompt, ai_response)
        st.success("Your interaction has been saved!")
    else:
        st.error("Please enter both your name and a prompt.")

# Instructor section for reviewing and grading
st.sidebar.title("Instructor's Panel")
password = st.sidebar.text_input("Enter admin password:", type="password")

if password == "admin123":  # Replace with a secure method for authentication
    st.sidebar.subheader("Review Interactions")
    data = load_data()
    if not data.empty:
        st.sidebar.write(data)

        # Select interaction for grading
        selected_idx = st.sidebar.number_input("Select row index to grade", min_value=0, max_value=len(data) - 1)
        new_score = st.sidebar.slider("Assign a score:", 0, 10, 5)

        if st.sidebar.button("Submit Score"):
            data.loc[selected_idx, "Score"] = new_score
            data.to_csv("student_interactions.csv", index=False)
            st.sidebar.success("Score updated successfully!")
    else:
        st.sidebar.write("No interactions found.")
else:
    st.sidebar.write("Enter admin password to access grading panel.")
