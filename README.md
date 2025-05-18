# Streamlit FastAPI Application

This project is a web application that combines FastAPI for the backend and Streamlit for the frontend. It serves as a template for building interactive web applications with a modern tech stack.

## Project Structure

```
streamlit-fastapi-app
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py
│   │   │   └── models.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend
│   ├── __init__.py
│   ├── app.py
│   ├── pages
│   │   ├── __init__.py
│   │   └── dashboard.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── api_client.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Backend

The backend is built using FastAPI and is structured as follows:

- **app/**: Contains the main application code.
  - **api/**: Contains the API endpoints and models.
  - **core/**: Contains core configuration and initialization code.
  - **main.py**: The entry point for the FastAPI application.

### Requirements

The backend dependencies are listed in `backend/requirements.txt`.

### Docker

The backend can be containerized using the `Dockerfile` located in the `backend` directory.

## Frontend

The frontend is built using Streamlit and is structured as follows:

- **app.py**: The entry point for the Streamlit application.
- **pages/**: Contains different pages of the Streamlit application.
- **utils/**: Contains utility functions for API calls and other helper functions.

### Requirements

The frontend dependencies are listed in `frontend/requirements.txt`.

### Docker

The frontend can be containerized using the `Dockerfile` located in the `frontend` directory.

## Running the Application

To run the application, use Docker Compose. The `docker-compose.yml` file defines the services for both the backend and frontend. 

1. Build the containers:
   ```
   docker-compose build
   ```

2. Start the application:
   ```
   docker-compose up
   ```

Visit `http://localhost:8501` to access the Streamlit application and interact with the FastAPI backend.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.