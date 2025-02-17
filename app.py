import openai
import streamlit as st
import pandas as pd
import datetime
from io import BytesIO
import numpy as np
from PIL import Image, UnidentifiedImageError
import random
import requests
import matplotlib.pyplot as plt
import PyPDF2

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

# Set max token limit (GPT-3.5 & GPT-4 support ~16,385 tokens, but we use less)
MAX_TEXT_LENGTH = 3000  # Limit input text to first 3,000 words (~12,000 tokens)

# Function to truncate long text
def truncate_text(text, max_words=MAX_TEXT_LENGTH):
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "...\n\n[Text truncated due to length]"
    return text

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
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.5
    )
    return response.choices[0].message["content"].strip()

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(uploaded_pdf):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_pdf)  # Read the PDF
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text if text.strip() else "No readable text found in PDF."
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"
        
# Prompt Engineering Assignment Page with Text Extraction
def prompt_engineering_assignment_page():
    st.title("Prompt Engineering Assignment: Warranty Analysis")

    # Step 1: Enter API Key & Student Name
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    student_name = st.text_input("Enter your name:")

    # Step 2: Upload Warranty Document
    st.subheader("Upload the Warranty Document (PDF Only)")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    extracted_text = ""
    truncated_text = ""
    
    if uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
        truncated_text = truncate_text(extracted_text)  # Truncate long text

        # Display extracted text (showing truncated if applicable)
        st.subheader("Extracted Warranty Text (Truncated if too long):")
        st.text_area("Text from the document:", truncated_text, height=200)

    # Step 3: Writing an Effective Prompt
    st.subheader("Write an Effective Prompt")
    prompt = st.text_area("Write your prompt here:")

    # Generate AI Response Button
    generate_button = st.button("Generate AI Response")

    if generate_button:
        if api_key and student_name and prompt and uploaded_file:
            full_prompt = f"""
            You are a warranty specialist assisting a customer. Below is the warranty document text:
            
            {truncated_text}
            
            The customer has this issue with their product:
            {prompt}
            
            Based on the warranty terms, determine if this issue qualifies for a claim. Explain why or why not.
            """

            try:
                response = generate_response(api_key, full_prompt)
                st.subheader("AI Warranty Evaluation:")
                st.markdown(response)
                save_interaction(student_name, prompt, response)
                st.success("Your interaction has been saved locally!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please provide your name, API key, warranty document, and a prompt.")

    # Download Student Logs
    if st.session_state.interactions:
        st.download_button(
            label="Download Interactions as Excel",
            data=generate_excel(),
            file_name=f"{student_name}_interactions.xlsx",
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
        st.write("""
        1. How does the regenerated image compare to the original?
        2. How does the mask size affect the quality of regeneration?
        3. What are the limitations of this lightweight inpainting method?
        """)

# Supervised and Unsupervised Learning Page
def supervised_unsupervised_page():
    st.title("Supervised and Unsupervised Learning")
    st.write("""
    This page introduces supervised and unsupervised machine learning concepts with interactive examples in finance and marketing.
    """)

    # Supervised Learning Section
    st.header("Supervised Learning")
    st.write("Supervised learning predicts outcomes based on labeled data.")
    st.write("### Example: Predicting Loan Approval")

    st.write("Select values for Income and Credit Score to see if a loan would be approved.")
    income = st.slider("Income (in $):", 2000, 20000, 8000, 100)
    credit_score = st.slider("Credit Score:", 300, 850, 650, 10)
    approval = "Approved" if (income > 5000 and credit_score > 600) else "Rejected"
    st.write(f"Loan Status: **{approval}**")

    # Unsupervised Learning Section
    st.header("Unsupervised Learning")
    st.write("Unsupervised learning identifies patterns in unlabeled data.")
    st.write("### Example: Clustering Products Based on Price and Rating")

    if 'product_data' not in st.session_state:
        st.session_state.product_data = pd.DataFrame({
            'Price': np.concatenate([
                np.random.randint(10, 100, 30),  # Cluster 1: Low-price products
                np.random.randint(100, 300, 40),  # Cluster 2: Mid-price products
                np.random.randint(300, 500, 30)  # Cluster 3: High-price products
            ]),
            'Rating': np.concatenate([
                np.random.uniform(1, 2.5, 30),  # Cluster 1: Lower ratings
                np.random.uniform(2.5, 4, 40),  # Cluster 2: Medium ratings
                np.random.uniform(4, 5, 30)  # Cluster 3: High ratings
            ]).round(1),
            'Cluster': np.concatenate([
                np.full(30, 1),  # Cluster 1
                np.full(40, 2),  # Cluster 2
                np.full(30, 3)  # Cluster 3
            ])
        })

    product_data = st.session_state.product_data
    selected_cluster = st.selectbox("Select a Cluster to Highlight:", product_data['Cluster'].unique())

    fig, ax = plt.subplots(figsize=(8, 6))  # Resized visualization
    for cluster in product_data['Cluster'].unique():
        cluster_points = product_data[product_data['Cluster'] == cluster]
        alpha = 1.0 if cluster == selected_cluster else 0.3
        ax.scatter(cluster_points['Price'], cluster_points['Rating'], label=f'Cluster {cluster}', alpha=alpha)
    ax.set_xlabel('Price ($)')
    ax.set_ylabel('Rating (1-5)')
    ax.legend()
    st.pyplot(fig)

    # Reflection Section
    st.header("Reflection Questions")
    st.write("""
    1. What factors might influence the loan approval decision?
    2. What insights can you gain about product clusters based on price and ratings?
    """)
    st.text_area("Your Reflections:")

# Generate AI Response with Custom Parameters
def generate_response_with_params(api_key, prompt, temperature, max_tokens):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message["content"].strip()

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
        {"review": "The food was overpriced.", "response": "We appreciate your feedback and will review our pricing."},
        {"review": "Can you recommend a gluten-free dessert?", "response": "Certainly! We have a delicious gluten-free chocolate cake."},
        {"review": "The delivery was late.", "response": "We sincerely apologize for the delay. We are working on improving our delivery times."},
        {"review": "The waiter was very rude.", "response": "We are sorry to hear about your experience. We will address this with our staff."},
        {"review": "I loved the ambiance, but the food was cold.", "response": "Thank you for the feedback! We are glad you enjoyed the ambiance and will work on serving hot food."},
        {"review": "The vegetarian options are limited.", "response": "We appreciate your input and will expand our vegetarian menu soon."}
    ]

    selected_examples = []
    for i, example in enumerate(examples):
        if st.checkbox(f"Include Example {i+1}: '{example['review']}'", value=True):
            selected_examples.append(example)

    # Parameter Tuning
    st.subheader("Step 2: Adjust Parameters")
    st.write("""
    Adjust the parameters below to influence how the model responds:
    - **Creativity (Temperature):** Higher values (e.g., 1.0) make responses more creative and random. Lower values (e.g., 0.0) make them more deterministic.
    - **Response Length (Max Tokens):** Adjust the length of the chatbot's response.
    """)
    temperature = st.slider("Creativity Level (Temperature)", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Maximum Response Length (Tokens)", 10, 100, 50)

    # Testing the Chatbot
    st.subheader("Step 3: Test the Fine-Tuned Chatbot")
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    student_name = st.text_input("Enter your name:")
    test_review = st.text_input("Enter a sample review:")

    if st.button("Generate Response"):
        if selected_examples and test_review and api_key and student_name:
            try:
                # Simulate response generation based on selected examples
                prompt = f"You are a chatbot trained to handle restaurant reviews. Here are some examples:\n"
                for example in selected_examples:
                    prompt += f"Review: {example['review']}\nResponse: {example['response']}\n"
                prompt += f"\nNow respond to this review:\nReview: {test_review}\nResponse:"

                response = generate_response_with_params(api_key, prompt, temperature, max_tokens)
                st.success(f"Chatbot Response: {response}")

                # Save interaction
                save_interaction(student_name, test_review, response)

            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please select examples, enter a review, provide your API key, and your name to test the chatbot.")

    # Provide Download Option for Interactions
    if st.session_state.interactions:
        st.subheader("Step 4: Download Your Interactions")
        st.write("Download your interactions as an Excel file and upload it to Canvas.")
        excel_data = generate_excel()
        st.download_button(
            label="Download Interactions",
            data=excel_data,
            file_name=f"{student_name}_interactions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Reflection Section
    st.subheader("Reflection Questions")
    st.write("""
    1. How did the selected examples influence the chatbot's response?
    2. How does adjusting the creativity level (temperature) affect the chatbot's behavior?
    3. What are the limitations of fine-tuning with a small dataset?
    4. What happens when you add or remove specific types of examples (e.g., complaints, compliments)?
    """)

# Initialize session state for interactions
if 'interactions' not in st.session_state:
    st.session_state.interactions = []

# Function to generate AI response
def fetch_ai_response(api_key, prompt, model, temperature, max_tokens):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message["content"].strip()

# Custom GPT Page
def custom_gpt_page():
    st.title("Custom GPT Assistant")
    st.sidebar.header("Customize Your GPT")
    
    # User input for model configuration
    persona = st.sidebar.text_area("Persona Instructions", "You are an AI tutor specializing in cybersecurity.")
    model = st.sidebar.selectbox("Choose Model", ["gpt-4", "gpt-3.5-turbo"])
    temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.7)
    max_tokens = st.sidebar.slider("Max Tokens", 50, 2000, 500)
    
    # Upload optional knowledge base
    uploaded_file = st.sidebar.file_uploader("Upload a Knowledge Base (TXT)", type=["txt"])
    kb_content = ""
    if uploaded_file is not None:
        kb_content = uploaded_file.read().decode("utf-8")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": persona + "\n" + kb_content}]
    
    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # User input
    user_input = st.text_area("Ask me anything:")
    if st.button("Send"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)
            
            response = fetch_ai_response(st.secrets["OPENAI_API_KEY"], user_input, model, temperature, max_tokens)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

# Navigation Sidebar
page = st.sidebar.selectbox(
    "Select a Page",
    [
        "Prompt Engineering",
        "Ethics in AI",
        "Self-Supervised Learning",
        "Supervised and Unsupervised Learning",
        "Fine-Tuning LLM Models",
        "Custom GPT Assistant"
    ],
    key="page_selector"
)

# Page routing
if page == "Prompt Engineering":
    prompt_engineering_assignment_page()
elif page == "Ethics in AI":
    ethics_in_ai_page()
elif page == "Self-Supervised Learning":
    self_supervised_learning_page()
elif page == "Supervised and Unsupervised Learning":
    supervised_unsupervised_page()
elif page == "Fine-Tuning LLM Models":
    fine_tuning_page()
elif page == "Custom GPT Assistant":
    custom_gpt_page()
