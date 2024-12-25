# Loan Prediction Chatbot Using Dialogflow  

This project demonstrates a **Loan Prediction Chatbot** built using **Dialogflow**, integrated with an ML model for loan eligibility prediction. The chatbot collects user details and predicts loan eligibility using an ML model deployed as a webhook.  

---

## Features  
- Predict loan eligibility based on user inputs like income, loan amount, CIBIL score, etc.  
- Integrated with Dialogflow to enable a conversational interface.  
- Uses **Flask** as a backend webhook to connect with the ML model.  
- Real-time testing and deployment using **ngrok**.  
- Deployed using Docker and GCP for scalability.  

---

## Tools & Technologies  
- **Machine Learning**: Scikit-learn for creating the loan prediction model.  
- **Dialogflow**: For building and training the chatbot.  
- **Flask**: To serve the webhook API.  
- **Ngrok**: For local testing of the webhook.  
- **Docker**: For containerizing the application.  
- **Google Cloud Platform (GCP)**: For hosting the webhook.  

---

## Requirements  
Make sure you have the following installed:  
- Python 3.7 or higher  
- Flask  
- Dialogflow account  
- Ngrok  
- Docker  
- GCP account  

---

## How to Run the Project  

### 1. Clone the Repository  
```bash  
git clone <repository-url>  
cd <repository-folder>  
