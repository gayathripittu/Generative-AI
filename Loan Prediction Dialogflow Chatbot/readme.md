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
```

### 2. Install Dependencies
Create a virtual environment and install the required packages:

```bash  
python -m venv venv  
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`  
pip install -r requirements.txt
```

### 3. Train and Save the ML Model
- Train your ML model and save it as a `.pkl` file.
- If you're using a scaler for normalization, save it as a `.pkl` file as well.

### 4. Start Flask Webhook
- Create a Flask app with a /predict route that processes requests from Dialogflow.
- Run the Flask app:
  
```bash 
python app.py  
```
Use Ngrok to expose the Flask server with a public URL.

### 5. Expose Localhost Using Ngrok
Run the following command to get a public URL for your webhook:

```bash 
ngrok http portnumber   
```

Use the generated public URL (e.g.,` https://your-ngrok-url.ngrok-free.app/predict`) in Dialogflow webhook settings.
Test locally using ngrok before deploying to GCP or any cloud provider.

### 6.Create and Integrate Dialogflow Chatbot

##### 1. Create a Dialogflow Agent:
  - Go to the Dialogflow Console.
  - Create a new agent.
  - Define intents (e.g., Start Intent, Collect Parameters, Submit Intent) to handle 
    conversations.
  - Set up entities for custom parameters (e.g., @sys.number for numerical inputs).
  - Enable webhook calls in the Fulfillment section and add the Ngrok URL as the webhook 
    endpoint.

##### 2.Configure Webhook:
Create a 'Dockerfile' and build the image:
  - Enable webhook calls in the Fulfillment section.
  - Add the public URL (e.g., from Ngrok or GCP) as the webhook endpoint.

##### 3.Integrate the Flask Webhook:
Create a 'Dockerfile' and build the image:
  - Ensure the Flask app processes the incoming JSON request and sends a proper response.


#### Commands

- **Build Docker Image:**
```bash 
docker build -t loan-prediction-chatbot .     
```
- **Run the Docker Container Locally**
```bash 
docker run -p 8080:8080 loan-prediction-chatbot     
```

- **Deploy to GCP:**
```bash 
gcloud run deploy loan-prediction-chatbot --image gcr.io/<your_project_id>/loan-prediction-chatbot --platform managed --region <your_region> --allow-unauthenticated
```

## Testing
- Test your agent in the Dialogflow console.
- Ensure that your webhook is called correctly and the responses are accurate.

## Usage
#### Interaction Flow
1. Start the chatbot:
  - User: "I want to check loan eligibility."
  - Chatbot: "I will need some details to predict loan eligibility. Let's begin!"
2. Provide required details as prompted by the bot.
3. Receive loan eligibility prediction.

##### Example

```bash
Chatbot: 🤖 What is your annual income?
User: 700000
Chatbot: 🤖 How much loan amount are you applying for?
User: 700000
Chatbot: 🤖 What is the loan term in months?
User: 45
Chatbot: 🤖 What is your CIBIL score?
User: 760
Chatbot: 🤖 Are you self-employed? (Yes or No)?
User: No
Chatbot: 🤖 🎉 Congratulations! Your loan application has been pre-approved! 🎉
```
