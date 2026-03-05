import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

# Configuration
DATA_PATH = 'd:/blood presser/data.csv'
MODEL_PATH = 'd:/blood presser/model.pkl'
SCALER_PATH = 'd:/blood presser/scaler.pkl'

def synthesize_data(n_samples=1000):
    print("Synthesizing individual-level data...")
    # Seed for reproducibility
    np.random.seed(42)
    
    # Demographics
    ages = np.random.randint(12, 85, n_samples)
    genders = np.random.choice(['Male', 'Female'], n_samples)
    
    # Blood Test Parameters (Synthesized based on clinical norms)
    # Hemoglobin (g/dL) - Normal: 13.5-17.5 (M), 12.0-15.5 (F)
    # RBC count (million cells/mcL) - Normal: 4.7-6.1 (M), 4.2-5.4 (F)
    # MCV (fL) - Normal: 80-100
    
    hb = []
    rbc = []
    mcv = []
    target = [] # 1 for Anemia, 0 for No Anemia
    
    for i in range(n_samples):
        is_female = (genders[i] == 'Female')
        
        # Determine if this sample will be "Anemic" (approx 20% prevalence in synthetic data)
        anemic = np.random.random() < 0.2
        target.append(1 if anemic else 0)
        
        if anemic:
            # Anemic ranges
            hb_val = np.random.uniform(7.0, 11.5 if is_female else 13.0)
            rbc_val = np.random.uniform(3.0, 4.0 if is_female else 4.5)
            mcv_val = np.random.uniform(60, 85)
        else:
            # Normal ranges
            hb_val = np.random.uniform(12.0 if is_female else 13.5, 16.0 if is_female else 18.0)
            rbc_val = np.random.uniform(4.2 if is_female else 4.7, 5.5 if is_female else 6.2)
            mcv_val = np.random.uniform(85, 100)
            
        hb.append(round(hb_val, 1))
        rbc.append(round(rbc_val, 2))
        mcv.append(round(mcv_val, 1))
        
    df = pd.DataFrame({
        'Age': ages,
        'Gender': genders,
        'Hemoglobin': hb,
        'RBC_Count': rbc,
        'MCV': mcv,
        'Anemia': target
    })
    
    # Encode Gender
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
    
    return df

def train():
    # We use some insights from the provided CSV for age/gender distribution if possible, 
    # but for this specific "flow" we need individual rows.
    df = synthesize_data(2000)
    
    X = df.drop('Anemia', axis=1)
    y = df['Anemia']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and scaler
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"Model saved to {MODEL_PATH}")
    print(f"Scaler saved to {SCALER_PATH}")

if __name__ == "__main__":
    train()
