from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the scaler and model
with open('app/scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open('app/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the numerical and categorical features
numerical_features = ['income_annum', 'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value', 'commercial_assets_value']
categorical_features = ['no_of_dependents', 'self_employed']

@app.route('/')
def hello():
    return 'Hello, World'

@app.route('/predict', methods=['POST'])
def predict():

    try:
        # Extract parameters from Dialogflow request (assuming they match your feature names)
        req = request.get_json(silent=True, force=True)
        print(req)
        income_annum = req.get('queryResult').get('parameters').get('income_annum')
        loan_amount = req.get('queryResult').get('parameters').get('loan_amount')
        loan_term = req.get('queryResult').get('parameters').get('loan_term')
        cibil_score = req.get('queryResult').get('parameters').get('cibil_score')
        residential_assets_value = req.get('queryResult').get('parameters').get('residential_assets_value')
        commercial_assets_value = req.get('queryResult').get('parameters').get('commercial_assets_value')
        no_of_dependents = req.get('queryResult').get('parameters').get('no_of_dependents')
        self_employed = req.get('queryResult').get('parameters').get('self_employed')

        # Prepare data for prediction
        data = {
            'income_annum': income_annum,
            'loan_amount': loan_amount,
            "loan_term": loan_term,
            "cibil_score": cibil_score,
            "residential_assets_value": residential_assets_value,
            "commercial_assets_value": commercial_assets_value,
            "no_of_dependents": no_of_dependents,
            "self_employed": self_employed
        }
        df = pd.DataFrame([data])
        
        df[numerical_features] = scaler.transform(df[numerical_features])
        prediction = model.predict(df[numerical_features + categorical_features])

        if int(prediction[0]) == 0:
            response = "Unfortunately, your loan application was not approved at this time"
        else:
            response = "Congratulations! Your loan application has been pre-approved"

        # Prepare response for Dialogflow
        return jsonify({
            "fulfillmentText": response 
        })

    except:
        return jsonify({
            "fulfillmentText": "An error occurred. Please try again."
        })

if __name__ == '__main__':
    app.run(debug=True)
