import streamlit as st
import pandas as pd
import datetime
import os
import requests

# Set page configuration
st.set_page_config(page_title="CoPilot App Manager", layout="wide")

# Using your image link from UNCG
image_url = "https://uncgcdn.blob.core.windows.net/wallpaper/Wallpaper_Minerva-UNCG_desktop_3840x2160.jpg"

# CSS to set background and font styles
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

def list_all_connections(api_key):
    """Lists all connections available in the workspace."""
    url = "https://api.copilot.com/v1/connections"  # Assuming this is a valid endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # Return connections as JSON

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error: {http_err}")
        st.error(f"Response content: {response.text}")
        raise
    except Exception as err:
        st.error(f"Unexpected error: {err}")
        raise

def create_connection(api_key, company_id=None, client_ids=None):
    """Creates a new app connection."""
    url = "https://api.copilot.com/v1/connections"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "companyId": company_id,
        "clientIds": client_ids  # Either companyId or clientIds must be provided
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
st.title("CoPilot Connections Manager")

# Input fields for API key, Company ID, and Client IDs
api_key = st.text_input("Enter your CoPilot API Key:", type="password")
company_id = st.text_input("Enter the Company ID (optional):")
client_ids = st.text_area("Enter Client IDs (comma-separated, optional):")

# Button to list all connections
if st.button("List All Connections"):
    if api_key:
        try:
            connections = list_all_connections(api_key)
            st.subheader("All Connections")
            st.write(connections)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please provide the API key.")

# Button to create a new connection
if st.button("Create New Connection"):
    if api_key:
        try:
            client_ids_list = [cid.strip() for cid in client_ids.split(",")] if client_ids else None
            connection = create_connection(api_key, company_id, client_ids_list)
            st.success("Connection created successfully!")
            st.write(connection)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please provide the API key.")
