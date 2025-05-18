import streamlit as st
import requests

# Set the title of the Streamlit app
st.title("Streamlit FastAPI Application")

# Define a function to call the FastAPI backend
def get_data_from_backend():
    response = requests.get("http://backend:8000/api/data")  # Adjust the endpoint as needed
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the backend.")
        return None

# Fetch data from the backend
data = get_data_from_backend()

# Display the data in the Streamlit app
if data:
    st.write("Data from FastAPI backend:")
    st.json(data)  # Display the data in a JSON format
else:
    st.write("No data available.")