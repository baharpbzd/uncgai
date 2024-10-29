import openai
import streamlit as st
import pandas as pd
import datetime

def generate_response(api_key, prompt):
    # Set the provided API key
    openai.api_key = api_key
    
    # Generate the AI response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or "gpt-4"
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

# Streamlit UI setup
st.title("AI Prompt Engineering Assignment")

# Input fields for the student's name, API key, and prompt
student_name = st.text_input("Enter your name:")
api_key = st.text_input("Enter your OpenAI API Key:", type="password")  # Masked input
prompt = st.text_area("Write your prompt:")

if st.button("Generate AI Response"):
    if student_name and api_key and prompt:
        try:
            # Generate AI response
            ai_response = generate_response(api_key, prompt)
            st.subheader("AI Response")
            st.write(ai_response)

            # Save the interaction to a CSV
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = pd.DataFrame([[student_name, prompt, ai_response, timestamp]],
                                columns=["Student", "Prompt", "AI_Response", "Timestamp"])
            data.to_csv("student_interactions.csv", mode="a", header=False, index=False)
            st.success("Your interaction has been saved!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please provide your name, API key, and a prompt.")
