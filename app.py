import os
import openai
import streamlit as st
import pandas as pd
import datetime
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gclient = gspread.authorize(creds)

# Open your Google Sheet
sheet = gclient.open("Student Interactions").sheet1  # Change the name if needed

def generate_response(prompt):
    # Generate a response using OpenAI's Chat API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4"
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()

def save_to_google_sheets(name, prompt, response, timestamp):
    # Save the interaction to Google Sheets
    sheet.append_row([name, prompt, response, timestamp])

def load_interactions():
    # Load all interactions from Google Sheets into a DataFrame
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# Streamlit UI setup
st.title("AI Prompt Engineering Assignment")

# Input fields for the student's name, prompt, and API key
student_name = st.text_input("Enter your name:")
api_key = st.text_input("Enter your OpenAI API Key:", type="password")  # Masked input
prompt = st.text_area("Write your prompt:")

if st.button("Generate AI Response"):
    if student_name and api_key and prompt:
        try:
            # Temporarily set the provided API key
            openai.api_key = api_key
            
            # Generate AI response
            ai_response = generate_response(prompt)
            st.subheader("AI Response")
            st.write(ai_response)

            # Save the interaction to Google Sheets
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_to_google_sheets(student_name, prompt, ai_response, timestamp)

            st.success("Your interaction has been saved!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please provide your name, API key, and a prompt.")

# Download section for instructors
st.sidebar.title("Instructor's Panel")
if st.sidebar.button("Download Interactions as CSV"):
    interactions_df = load_interactions()

    # Convert DataFrame to CSV and create a download button
    csv = interactions_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download Interactions",
        data=csv,
        file_name="student_interactions.csv",
        mime="text/csv"
    )
