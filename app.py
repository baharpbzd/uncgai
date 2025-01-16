import openai  
import streamlit as st
import pandas as pd
import datetime
from io import BytesIO
import numpy as np
from PIL import Image, UnidentifiedImageError
import random
import requests

# Set page configuration
st.set_page_config(page_title="AI Education App", layout="wide")

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

# Sidebar: Theme Selection
st.sidebar.title("Accessibility Mode")
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"], key="theme_radio")

# Update theme in session state if changed
if theme != st.session_state.theme:
    st.session_state.theme = theme

# Apply Theme-based Styling
if st.session_state.theme == 'Light':
    page_bg_color = "#FFFFFF"
    font_color = "#000000"
    sidebar_bg_color = "#F0F0F0"
    button_bg_color = "#4CAF50"
    button_hover_color = "#3E8E41"
    input_bg_color = "#FFFFFF"
    input_focus_color = "#4CAF50"
    dropdown_bg_color = "#FFFFFF"
    dropdown_text_color = "#000000"
    dropdown_hover_bg_color = "#E0E0E0"
else:
    page_bg_color = "#2E2E2E"
    font_color = "#FFFFFF"
    sidebar_bg_color = "#1E1E1E"
    button_bg_color = "#007BFF"
    button_hover_color = "#0056b3"
    input_bg_color = "#3E3E3E"
    input_focus_color = "#007BFF"
    dropdown_bg_color = "#444444"
    dropdown_text_color = "#FFFFFF"
    dropdown_hover_bg_color = "#555555"

# CSS Styling for Selectbox and Dropdown Menu Customization
page_style = f"""
    <style>
    .stApp {{
        background-color: {page_bg_color};
    }}
    h1, h2, h3, h4, h5, p, div {{
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 18px;
        color: {font_color};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg_color};
    }}
    section[data-testid="stSidebar"] * {{
        color: {font_color} !important;
    }}
    input, textarea {{
        background-color: {input_bg_color};
        color: {font_color};
        border: 1px solid #555555; /* Neutral border color */
        border-radius: 5px;
        padding: 5px;
    }}
    input:focus, textarea:focus {{
        border: 1px solid {input_focus_color};
        outline: none;
    }}
    button {{
        background-color: {button_bg_color} !important;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
        transition: background-color 0.3s;
    }}
    button:hover {{
        background-color: {button_hover_color} !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: {dropdown_bg_color};
        color: {dropdown_text_color};
        border-radius: 5px;
        padding: 10px;
        border: 1px solid {input_focus_color};
    }}
    div[data-baseweb="select"] > div:hover {{
        background-color: {dropdown_hover_bg_color};
    }}
    div[role="listbox"] {{
        background-color: {dropdown_bg_color};
    }}
    div[role="listbox"] ul li {{
        color: {dropdown_text_color};
    }}
    div[role="listbox"] ul li:hover {{
        background-color: {dropdown_hover_bg_color};
    }}
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# Initialize session state to store interactions
if 'interactions' not in st.session_state:
    st.session_state.interactions = []

# Save interaction locally in session state
def save_interaction(student_name, prompt, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.interactions.append({
        "Timestamp": timestamp,
        "Student Name": student_name,
        "Prompt": prompt,
        "AI Response": response
    })

# Generate Excel from interactions
def generate_excel():
    df = pd.DataFrame(st.session_state.interactions)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Interactions')
    return output.getvalue()

# Generate AI Response with OpenAI API
def generate_response(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()
    return response.choices[0].message["content"].strip()

# Prompt Engineering Page
def prompt_engineering_page():
    st.title("Prompt Engineering")
    st.write("This page is dedicated to teaching students about Prompt Engineering.")

    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    student_name = st.text_input("Enter your name:", key="student_name")
    prompt = st.text_area("Write a prompt to generate an AI response:")

    generate_button = st.button("Generate AI Response")

    if generate_button:
        if api_key and student_name and prompt:
            try:
                response = generate_response(api_key, prompt)
                st.markdown(
                    f"""
                    <div style="
                        background-color: {page_bg_color};
                        padding: 15px;
                        border-radius: 10px;
                        margin-top: 10px;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                        color: {font_color};">
                        {response}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                save_interaction(student_name, prompt, response)
                st.success("Your interaction has been saved locally!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please provide your name, API key, and a prompt.")

    if st.session_state.interactions:
        st.download_button(
            label="Download Interactions as Excel",
            data=generate_excel(),
            file_name="interactions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Ethics in AI Page
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

# Set page configuration
st.set_page_config(page_title="AI Education App", layout="wide")

# Initialize session state for responses
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Function to save responses
def save_responses(student_name, q1, q2, q3):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.responses.append({
        "Timestamp": timestamp,
        "Student Name": student_name,
        "Q1": q1,
        "Q2": q2,
        "Q3": q3
    })

# Generate Excel from responses
def generate_excel_responses():
    df = pd.DataFrame(st.session_state.responses)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Responses')
    return output.getvalue()

# Self-Supervised Learning Page
def self_supervised_learning_page():
    st.title("Introduction to Self-Supervised Learning")
    st.write("""
    Self-supervised learning (SSL) is a way for machines to learn from data without labels. 
    In this exercise, you will upload an image, mask a portion of it, and observe how AI regenerates the missing part using a lightweight OpenCV method.
    """)

    # Step 1: Upload an Image
    st.subheader("Step 1: Upload an Image")
    uploaded_file = st.file_uploader("Upload an Image (JPG or PNG)", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        original_image = Image.open(uploaded_file).convert("RGB")
        st.image(original_image, caption="Original Image", use_container_width=True)

        # Step 2: Adjust Mask Size
        st.subheader("Step 2: Adjust Mask Size")
        mask_size = st.slider("Select Mask Size (percentage of image):", 10, 50, 30)

        def mask_image(image, mask_percentage):
            image = np.array(image)
            height, width, _ = image.shape
            mask = np.zeros((height, width), dtype=np.uint8)
            mask_height = int((mask_percentage / 100) * height)
            mask_width = int((mask_percentage / 100) * width)

            start_x = random.randint(0, width - mask_width)
            start_y = random.randint(0, height - mask_height)

            mask[start_y:start_y + mask_height, start_x:start_x + mask_width] = 255

            masked_image = image.copy()
            masked_image[start_y:start_y + mask_height, start_x:start_x + mask_width, :] = 0
            return Image.fromarray(masked_image), mask

        masked_image, mask = mask_image(original_image, mask_size)
        st.image(masked_image, caption=f"Masked Image ({mask_size}% masked)", use_container_width=True)

        # Step 3: Regenerate the Masked Area Using OpenCV
        st.subheader("Step 3: Regenerate the Masked Area")
        if st.button("Regenerate Masked Area"):
            try:
                import cv2
                original_np = np.array(original_image)
                inpainted_image = cv2.inpaint(
                    original_np, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA
                )
                st.image(Image.fromarray(inpainted_image), caption="Regenerated Image", use_container_width=True)
            except Exception as e:
                st.error(f"Error during inpainting: {str(e)}")

    # Reflection Questions
    st.write("### Reflection Questions:")
    st.write("Please answer the following questions. Your responses will be saved and can be downloaded as an Excel file for submission.")
    student_name = st.text_input("Enter your name:", key="student_name")
    q1 = st.text_area("1. How does the regenerated image compare to the original?", key="q1")
    q2 = st.text_area("2. How does the mask size affect the quality of regeneration?", key="q2")
    q3 = st.text_area("3. What are the limitations of this lightweight inpainting method?", key="q3")

    if st.button("Save and Download Responses"):
        if student_name and q1 and q2 and q3:
            save_responses(student_name, q1, q2, q3)
            excel_data = generate_excel_responses()
            file_name = f"{student_name}_responses_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            st.download_button(
                label="Download Responses as Excel",
                data=excel_data,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("Your responses have been saved and are ready for download!")
        else:
            missing_fields = []
            if not student_name:
                missing_fields.append("name")
            if not q1:
                missing_fields.append("answer to question 1")
            if not q2:
                missing_fields.append("answer to question 2")
            if not q3:
                missing_fields.append("answer to question 3")
            st.error(f"Please provide the following: {', '.join(missing_fields)}.")

# Integrate Self-Supervised Learning Page into Navigation
page = st.sidebar.selectbox("Select a Page", ["Prompt Engineering", "Ethics in AI", "Self-Supervised Learning"], key="page_selector")

if page == "Prompt Engineering":
    prompt_engineering_page()
elif page == "Ethics in AI":
    ethics_in_ai_page()
elif page == "Self-Supervised Learning":
    self_supervised_learning_page()
