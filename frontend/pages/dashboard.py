from streamlit import st
import requests

API_URL = "http://localhost:8000/api"  # Adjust the URL as needed

def fetch_data():
    response = requests.get(f"{API_URL}/data")  # Replace with your actual endpoint
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data from the backend.")
        return None

def display_dashboard(data):
    st.title("Dashboard")
    if data:
        st.write(data)  # Customize how you want to display the data
    else:
        st.write("No data available.")

def main():
    data = fetch_data()
    display_dashboard(data)

if __name__ == "__main__":
    main()