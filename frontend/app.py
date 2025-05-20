import streamlit as st
from utils.api_client import APIClient

# Set the title of the Streamlit app
st.title("Streamlit FastAPI Application")

# Create API client - use "backend" as hostname when using Docker
api_client = APIClient(base_url="http://backend:8000")

# For local development outside Docker:
# api_client = APIClient(base_url="http://localhost:8000")

# Fetch data from the backend
data = api_client.get_data()

# Display the data in the Streamlit app
if data:
    st.write("Data from FastAPI backend:")
    st.json(data)  # Display the data in a JSON format
else:
    st.write("No data available. Make sure the backend is running.")