import pickle
import numpy as np

MODEL_PATH = 'd:/blood presser/model.pkl'
SCALER_PATH = 'd:/blood presser/scaler.pkl'

def test_model():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

    # Test cases: [Age, Gender, Hemoglobin, RBC_Count, MCV]
    # Gender: 0=Male, 1=Female
    test_cases = [
        {"name": "Normal Male", "data": [30, 0, 15.0, 5.0, 90]},
        {"name": "Anemic Female", "data": [25, 1, 8.5, 3.2, 70]},
        {"name": "Normal Female", "data": [45, 1, 13.0, 4.5, 92]},
        {"name": "Anemic Male", "data": [60, 0, 10.0, 3.8, 75]}
    ]

    for tc in test_cases:
        features = np.array([tc['data']])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        prob = model.predict_proba(features_scaled)[0]
        
        print(f"Test Case: {tc['name']}")
        print(f"  Input: {tc['data']}")
        print(f"  Result: {'Anemia' if prediction == 1 else 'Normal'}")
        print(f"  Confidence: {prob[prediction]*100:.2f}%")
        print("-" * 30)

if __name__ == "__main__":
    test_model()
