import openai
import streamlit as st
import pandas as pd
import datetime
from io import BytesIO
import numpy as np
from PIL import Image
import random
import matplotlib.pyplot as plt

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
else:
    page_bg_color = "#2E2E2E"
    font_color = "#FFFFFF"
    sidebar_bg_color = "#1E1E1E"

page_style = f"""
    <style>
    .stApp {{
        background-color: {page_bg_color};
    }}
    h1, h2, h3, h4, h5, p, div {{
        font-family: 'Arial', sans-serif;
        color: {font_color};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg_color};
    }}
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# Fine-Tuning LLM Models Page
def fine_tuning_page():
    st.title("Fine-Tuning LLM Models")
    st.write("""
    This page introduces fine-tuning large language models (LLMs) in a simplified, interactive way.
    Fine-tuning allows AI to specialize for specific tasks by adjusting its responses using example data.
    """)

    # Scenario Description
    st.subheader("Scenario: Fine-Tuning a Chatbot for Restaurant Reviews")
    st.write("""
    Imagine we are customizing a chatbot to handle restaurant reviews. You can select training examples 
    and adjust parameters to observe how the chatbot's responses change.
    """)

    # Dataset Customization
    st.subheader("Step 1: Select Training Examples")
    examples = [
        {"review": "The pasta was amazing!", "response": "Thank you! We're thrilled you enjoyed it."},
        {"review": "The service was slow.", "response": "We apologize for the delay and will work to improve."},
        {"review": "Do you have vegan options?", "response": "Yes, we offer several vegan dishes. Let me assist you!"},
        {"review": "The ambiance was perfect.", "response": "Thank you! We're glad you liked the atmosphere."},
        {"review": "The food was overpriced.", "response": "We appreciate your feedback and will review our pricing."}
    ]

    selected_examples = []
    for i, example in enumerate(examples):
        if st.checkbox(f"Include Example {i+1}: '{example['review']}'", value=True):
            selected_examples.append(example)

    # Parameter Tuning
    st.subheader("Step 2: Adjust Parameters")
    temperature = st.slider("Creativity Level (Temperature)", 0.0, 1.0, 0.7)
    max_length = st.slider("Maximum Response Length", 10, 100, 50)

    # Testing the Chatbot
    st.subheader("Step 3: Test the Fine-Tuned Chatbot")
    test_review = st.text_input("Enter a sample review:")

    if st.button("Generate Response"):
        if selected_examples and test_review:
            # Simulate response generation based on selected examples
            matched_response = None
            for example in selected_examples:
                if test_review.lower() in example['review'].lower():
                    matched_response = example['response']
                    break

            if matched_response:
                st.success(f"Chatbot Response: {matched_response}")
            else:
                st.warning("Chatbot Response: I'm sorry, I don't have enough information to respond to that.")
        else:
            st.error("Please select examples and enter a review to test the chatbot.")

    # Reflection Section
    st.subheader("Reflection Questions")
    st.write("""
    1. How did the selected examples influence the chatbot's response?
    2. How does adjusting the creativity level (temperature) affect the responses?
    3. What are the limitations of using a small dataset for fine-tuning?
    """)
    st.text_area("Your Reflections:")

# Navigation
page = st.sidebar.selectbox("Select a Page", ["Prompt Engineering", "Ethics in AI", "Self-Supervised Learning", "Supervised and Unsupervised Learning", "Fine-Tuning LLM Models"], key="page_selector")

if page == "Prompt Engineering":
    prompt_engineering_page()
elif page == "Ethics in AI":
    ethics_in_ai_page()
elif page == "Self-Supervised Learning":
    self_supervised_learning_page()
elif page == "Supervised and Unsupervised Learning":
    supervised_unsupervised_page()
elif page == "Fine-Tuning LLM Models":
    fine_tuning_page()
