import openai
import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

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
    page_bg_color = "#FFFFFF"  # White background
    font_color = "#000000"  # Black text
    sidebar_bg_color = "#F0F0F0"  # Light gray sidebar background
    button_bg_color = "#4CAF50"  # Green button (light theme)
    input_bg_color = "#FFFFFF"  # White input fields
else:
    page_bg_color = "#333333"  # Dark background
    font_color = "#FFFFFF"  # White text
    sidebar_bg_color = "#1E1E1E"  # Dark sidebar background
    button_bg_color = "#1F7A8C"  # Teal button (dark theme)
    input_bg_color = "#555555"  # Dark input fields

# CSS Styling for Custom Dropdown and Theme
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
    }}
    button {{
        background-color: {button_bg_color} !important;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }}

    /* Customize the dropdown button */
    div[data-baseweb="select"] > div {{
        background-color: #228B22;  /* Forest Green button */
        color: white;  /* White text */
    }}
    div[data-baseweb="select"] > div:hover {{
        background-color: #1E7B1E;  /* Darker green on hover */
    }}

    /* Customize the expanded dropdown menu */
    ul[data-baseweb="menu"] {{
        background-color: #228B22;  /* Forest Green background for menu */
        border-radius: 5px;
    }}
    ul[data-baseweb="menu"] li {{
        color: white;  /* White text for dropdown items */
    }}
    ul[data-baseweb="menu"] li:hover {{
        background-color: #1E7B1E;  /* Darker green on hover */
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

# Prompt Engineering Page
def prompt_engineering_page():
    st.title("Prompt Engineering")
    st.write("This page is dedicated to teaching students about Prompt Engineering.")

    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    student_name = st.text_input("Enter your name:")
    prompt = st.text_area("Write a prompt to generate an AI response:")

    generate_button = st.button("Generate AI Response")

    if generate_button:
        if api_key and student_name and prompt:
            try:
                response = generate_response(api_key, prompt)
                st.markdown(
                    f"""
                    <div style="
                        background-color: #FFFFFF;
                        padding: 15px;
                        border-radius: 10px;
                        margin-top: 10px;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                        color: #000000;">
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

# Generate AI Response with OpenAI API
def generate_response(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

# Sidebar Navigation
page = st.sidebar.selectbox("Select a Page", ["Prompt Engineering", "Ethics in AI"])

if page == "Prompt Engineering":
    prompt_engineering_page()
elif page == "Ethics in AI":
    ethics_in_ai_page()
