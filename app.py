import openai
import streamlit as st
import pandas as pd
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
    page_bg_color = "#FFFFFF"
    font_color = "#000000"
    sidebar_bg_color = "#F0F0F0"
else:
    page_bg_color = "#333333"
    font_color = "#FFFFFF"
    sidebar_bg_color = "#1E1E1E"

# CSS Styling for consistent theme
page_style = f"""
    <style>
    .stApp {{
        background-color: {page_bg_color};
    }}
    h1, h2, h3, h4, h5, p, div {{
        color: {font_color};
        font-family: 'Arial', sans-serif;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg_color};
    }}
    section[data-testid="stSidebar"] * {{
        color: {font_color} !important;
    }}
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# Initialize session state for interactions
if 'interactions' not in st.session_state:
    st.session_state.interactions = []

# Function to save interactions
def save_interaction(student_name, prompt, response):
    st.session_state.interactions.append({
        "Student Name": student_name,
        "Prompt": prompt,
        "AI Response": response
    })

# Function to generate AI response
def generate_response(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

# Function to generate an Excel file
def generate_excel():
    df = pd.DataFrame(st.session_state.interactions)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Interactions')
    return output.getvalue()

# Page: Introduction to Generative AI
def introduction_page():
    st.title("Introduction to Generative AI")
    st.write("Learn the basics of Generative AI, how different models work, and how they answer questions.")
    st.subheader("Different Generative AI Models")
    st.write("Explore models like GPT, DALL-E, and more.")
    st.subheader("How They Work")
    st.write("Understand the mechanisms behind these models, such as transformers and attention.")
    st.subheader("Assignment")
    st.write("Complete Quiz 1 and Homework 1.")

# Page: Prompt Engineering
def prompt_engineering_page():
    st.title("Prompt Engineering")
    st.write("Learn how to improve AI responses with effective prompts.")
    st.subheader("Examples and Techniques")
    st.write("See examples of prompt engineering and how it enhances AI output.")
    st.subheader("Assignment")
    st.write("Submit Homework 2.")

    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    student_name = st.text_input("Enter your name:")
    prompt = st.text_area("Write a prompt to generate an AI response:")

    if st.button("Generate AI Response"):
        if api_key and student_name and prompt:
            response = generate_response(api_key, prompt)
            st.write(response)
            save_interaction(student_name, prompt, response)
            st.success("Your interaction has been saved!")

    if st.session_state.interactions:
        st.download_button(
            label="Download Interactions as Excel",
            data=generate_excel(),
            file_name="interactions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Page: Business and Societal Impacts
def business_impact_page():
    st.title("Business and Societal Impacts of Generative AI")
    st.write("Discuss how Generative AI will disrupt business and societal norms.")
    st.subheader("Impact on Business Applications")
    st.write("Learn how AI is transforming industries like marketing, HR, and finance.")
    st.subheader("Misinformation and Regulation")
    st.write("Understand the challenges and regulatory considerations.")
    st.subheader("Assignment")
    st.write("Submit Homework 3.")

# Page: Ethics and Legal Issues
def ethics_page():
    st.title("Ethical, Legal, and Privacy Issues")
    st.write("Explore the ethical considerations and legal challenges of using Generative AI.")
    st.subheader("Bias and Fairness in AI Models")
    st.write("Learn how biases in data can affect AI models.")
    st.subheader("Privacy and Intellectual Property")
    st.write("Discuss privacy concerns and IP issues.")
    st.subheader("Assignment")
    st.write("Take Quiz 2.")

# Page: Applications of Generative AI
def applications_page():
    st.title("Applications of Generative AI")
    st.write("Explore how Generative AI is used in creative content generation, business applications, and personal development.")
    st.subheader("Examples in Business")
    st.write("Marketing, sales, HR, and more.")
    st.subheader("Assignment")
    st.write("Complete Quiz 3 and Homework 4.")

# Page: Project Tracker
def project_tracker_page():
    st.title("Course Project Tracker")
    st.write("Track your progress on the final course project.")
    st.subheader("Weekly Milestones")
    st.write("Make sure to meet each milestone for timely project completion.")
    st.subheader("Project Guidelines")
    st.write("Refer to the guidelines to ensure your project aligns with course objectives.")

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Select a Page",
    ["Introduction to Generative AI", "Prompt Engineering", "Business and Societal Impacts",
     "Ethics and Legal Issues", "Applications of Generative AI", "Project Tracker"]
)

# Page Navigation
if page == "Introduction to Generative AI":
    introduction_page()
elif page == "Prompt Engineering":
    prompt_engineering_page()
elif page == "Business and Societal Impacts":
    business_impact_page()
elif page == "Ethics and Legal Issues":
    ethics_page()
elif page == "Applications of Generative AI":
    applications_page()
elif page == "Project Tracker":
    project_tracker_page()
