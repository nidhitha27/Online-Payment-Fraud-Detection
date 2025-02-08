import numpy as np
from tensorflow.keras.models import load_model  # Use load_model from TensorFlow, not pickle
from flask import Flask, render_template, request
import logging

# Initialize Flask app
app = Flask(__name__)
# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the trained model (use TensorFlow's load_model function)
model_path = "static/model.h5"
try:
    model = load_model(model_path)  # Assuming your model is saved as .h5 file
    logging.info(f"Model loaded successfully from {model_path}")
except Exception as e:
    logging.error(f"Error loading model from {model_path}: {e}")

@app.route('/')
def home():
    """Render the home page with the input form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Get input values from the form
        transaction_type = request.form['type']
        amount = float(request.form['amount'])
        oldbalanceOrg = float(request.form['oldbalanceOrg'])
        newbalanceOrig = float(request.form['newbalanceOrig'])

        # Map the transaction type to an integer value
        transaction_mapping = {
            "CASH_OUT": 1,
            "PAYMENT": 2,
            "CASH_IN": 3,
            "TRANSFER": 4,
            "DEBIT": 5
        }
        val = transaction_mapping.get(transaction_type, 0)  # Default to 0 if type is invalid

        # Validate input data
        if val == 0 or amount < 0 or oldbalanceOrg < 0 or newbalanceOrig < 0:
            return render_template('index.html', prediction="Invalid input values provided.")

        # Log the received inputs
        logging.info(f"Received input - Type: {transaction_type}, Amount: {amount}, Old Balance: {oldbalanceOrg}, New Balance: {newbalanceOrig}")

        # Create input array for prediction
        input_array = np.array([[val, amount, oldbalanceOrg, newbalanceOrig]])

        # Make prediction using the loaded model
        prediction = model.predict(input_array)

        # Extract the predicted output value
        output = prediction[0][0]  # Assuming your model's output is a scalar value

        # Convert output to binary prediction (0 or 1)
        prediction_result = "Fraudulent" if output > 0.5 else "Non-Fraudulent"

        # Log the prediction
        logging.info(f"Prediction result: {prediction_result}, Probability: {output:.2f}")

        return render_template('index.html', prediction=f"Transaction is {prediction_result}. (Probability: {output:.2f})")
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return render_template('index.html', prediction=f"Error: {str(e)}")

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
