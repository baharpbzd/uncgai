import streamlit as st
import pandas as pd
import datetime
import os
import requests

# Set page configuration
st.set_page_config(page_title="CoPilot App Management", layout="wide")

# Using your image link from UNCG
image_url = "https://uncgcdn.blob.core.windows.net/wallpaper/Wallpaper_Minerva-UNCG_desktop_3840x2160.jpg"

# CSS for background and fonts
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("{image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}

h1, h2, h3, h4, h5, h6, p, div {{
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    font-size: 18px;
    color: black;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

def list_app_connections(api_key, install_id):
    """Lists all app connections for the specified manual app install."""
    url = f"https://api.copilot.com/v1/installs/{install_id}/connections"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for non-2xx responses
        return response.json()  # Return the list of connections as JSON

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error: {http_err}")
        st.error(f"Response content: {response.text}")
        raise
    except Exception as err:
        st.error(f"Unexpected error: {err}")
        raise

def create_app_connection(api_key, install_id, company_id=None, client_ids=None):
    """Creates an app connection for a manual app install."""
    url = f"https://api.copilot.com/v1/installs/{install_id}/connections"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "companyId": company_id,
        "clientIds": client_ids  # Either companyId or clientIds must be non-null
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()  # Return the created connection as JSON

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error: {http_err}")
        st.error(f"Response content: {response.text}")
        raise
    except Exception as err:
        st.error(f"Unexpected error: {err}")
        raise

# Streamlit UI setup
st.title("CoPilot App Connections Manager")

# Input fields for API key, install ID, company ID, and client IDs
api_key = st.text_input("Enter your CoPilot API Key:", type="password")
install_id = st.text_input("Enter the Install ID:")
company_id = st.text_input("Enter the Company ID (optional):")
client_ids = st.text_area("Enter Client IDs (comma-separated, optional):")

# Button to list app connections
if st.button("List App Connections"):
    if api_key and install_id:
        try:
            connections = list_app_connections(api_key, install_id)
            st.subheader("App Connections")
            st.write(connections)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please provide both the API key and Install ID.")

# Button to create an app connection
if st.button("Create App Connection"):
    if api_key and install_id:
        try:
            client_ids_list = [cid.strip() for cid in client_ids.split(",")] if client_ids else None
            connection = create_app_connection(api_key, install_id, company_id, client_ids_list)
            st.success("App connection created successfully!")
            st.write(connection)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please provide the API key, Install ID, and at least one of Company ID or Client IDs.")
