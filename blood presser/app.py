from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load model and scaler
MODEL_PATH = 'd:/blood presser/model.pkl'
SCALER_PATH = 'd:/blood presser/scaler.pkl'

model = None
scaler = None

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

def get_clinical_recommendations(prediction, hb, rbc):
    if prediction == 1:
        return {
            "interpretation": "Anemia Detected",
            "description": f"The model predicts the presence of anemia. Your hemoglobin level ({hb} g/dL) and RBC count ({rbc} M/mcL) are below the normal range adjusted for your demographic.",
            "recommendations": [
                "Consult a healthcare professional for a complete blood count (CBC) and further diagnostic tests.",
                "Incorporate iron-rich foods such as spinach, red meat, and legumes into your diet.",
                "Consider iron supplements if prescribed by a doctor.",
                "Monitor for symptoms like fatigue, dizziness, or shortness of breath."
            ],
            "severity": "Moderate (Based on input parameters)"
        }
    else:
        return {
            "interpretation": "No Anemia Detected",
            "description": "The model indicates that your blood parameters are within the healthy range for anemia screening.",
            "recommendations": [
                "Maintain a balanced diet rich in vitamins and minerals.",
                "Continue regular health check-ups.",
                "Stay hydrated and maintain an active lifestyle."
            ],
            "severity": "Normal"
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        data = request.json
        # Features: [Age, Gender, Hemoglobin, RBC_Count, MCV]
        # Gender encoding: 0 for Male, 1 for Female
        gender_code = 1 if data['gender'].lower() == 'female' else 0
        features = np.array([[
            float(data['age']),
            gender_code,
            float(data['hemoglobin']),
            float(data['rbc_count']),
            float(data['mcv'])
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        confidence = float(probabilities[prediction]) * 100
        
        result = get_clinical_recommendations(int(prediction), data['hemoglobin'], data['rbc_count'])
        result['confidence'] = round(confidence, 2)
        result['is_anemic'] = bool(prediction)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
