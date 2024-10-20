# Calcom Chatbot: Meeting Scheduler

This project is a **Calcom Chatbot** designed to interact with users and manage meeting bookings through natural language commands. The chatbot allows users to create, get, update, or cancel bookings using the **Cal.com API**. It leverages **Streamlit** for the front-end interface and is deployed on **Google Cloud** using **Docker**.

## Project Overview

The chatbot interacts with the **Cal.com API** to perform various meeting scheduling tasks:

- **Create bookings**: Schedule meetings by extracting required details such as attendee names, emails, and meeting times from user input.
- **Get bookings**: Retrieve existing booking details using natural language queries.
- **Update bookings**: Modify details of already scheduled meetings.
- **Cancel bookings**: Remove bookings upon user request.

### Key Features

- **Natural Language Processing**: The chatbot processes user inputs to extract relevant booking parameters.
- **Streamlit Front-end**: Provides an interactive UI for users to manage their meetings.
- **Google Cloud Deployment**: The application is containerized using Docker and deployed on **Google Cloud** for high availability.

## Tools and Technologies

- **Python**: Core development language.
- **Streamlit**: Front-end framework for building interactive web apps.
- **Cal.com API**: Backend API used for booking management.
- **Docker**: Containerization for easy deployment.
- **Google Cloud**: Hosting platform.

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2. **Streamlit**: Install Streamlit via pip:
   ```bash
   pip install streamlit
3. Cal.com API Key: You need a [Cal.com](https://cal.com/) account and API credentials. Set up your Cal.com API by signing up at Cal.com, and retrieve your API key from the developer dashboard.
4. Docker: If you plan to use Docker for deployment or running locally, install it from [Docker's official site](https://docs.docker.com/engine/install/).

## Running the Project
Once you have the prerequisites set up:

1. Clone the repository:
```bash
git clone <repository_url>
cd <repository_name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3.Set up environment variables for Cal.com API and Google Cloud credentials by creating a .env file in the root directory:
```bash
CALCOM_API_KEY=<your_api_key>
GOOGLE_CLOUD_API_KEY=<your_google_cloud_api_key>
```

## Run the Streamlit app:
```bash
streamlit run calc_main.py
Open your browser and navigate to http://localhost:8501 to interact with the chatbot.
```

## Deployment
The application has been containerized using Docker and deployed on Google Cloud for scalable access.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
