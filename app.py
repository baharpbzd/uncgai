import openai
import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="AI Education App", layout="wide")

# CSS for background and fonts
image_url = "https://uncgcdn.blob.core.windows.net/wallpaper/Wallpaper_Minerva-UNCG_desktop_3840x2160.jpg"
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("{image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}

h1, h2, h3, h4, h5, p, div {{
    font-family: 'Arial', sans-serif';
    font-weight: bold;
    font-size: 18px;
    color: black;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state to store interactions
if 'interactions' not in st.session_state:
    st.session_state.interactions = []

# Function to save interaction locally
def save_interaction(student_name, prompt, response):
    """Save interaction to session state."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.interactions.append({
        "Timestamp": timestamp,
        "Student Name": student_name,
        "Prompt": prompt,
        "AI Response": response
    })

# Function to generate downloadable Excel file
def generate_excel():
    """Generate an Excel file from the interactions."""
    df = pd.DataFrame(st.session_state.interactions)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Interactions')
    return output.getvalue()

# Function for Prompt Engineering Page
def prompt_engineering_page():
    st.title("Prompt Engineering")
    st.write("This page is dedicated to teaching students about Prompt Engineering.")

    # Input fields for API key, student name, and prompt
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    student_name = st.text_input("Enter your name:")
    prompt = st.text_area("Write a prompt to generate an AI response:")

    if st.button("Generate AI Response"):
        if api_key and student_name and prompt:
            try:
                response = generate_response(api_key, prompt)
                st.subheader("AI Response")
                st.write(response)

                # Save the interaction locally
                save_interaction(student_name, prompt, response)
                st.success("Your interaction has been saved locally!")

            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please provide your name, API key, and a prompt.")

    # Download button for Excel file
    if st.session_state.interactions:
        st.download_button(
            label="Download Interactions as Excel",
            data=generate_excel(),
            file_name="interactions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Function for Ethics in AI Page
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
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a Page", ["Prompt Engineering", "Ethics in AI"])

# Render the selected page
if page == "Prompt Engineering":
    prompt_engineering_page()
elif page == "Ethics in AI":
    ethics_in_ai_page()
