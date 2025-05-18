import requests

BASE_URL = "http://localhost:8000"  # Update with your FastAPI backend URL

def get_data(endpoint: str):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    response.raise_for_status()
    return response.json()

def post_data(endpoint: str, data: dict):
    response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
    response.raise_for_status()
    return response.json()

def put_data(endpoint: str, data: dict):
    response = requests.put(f"{BASE_URL}/{endpoint}", json=data)
    response.raise_for_status()
    return response.json()

def delete_data(endpoint: str):
    response = requests.delete(f"{BASE_URL}/{endpoint}")
    response.raise_for_status()
    return response.json()