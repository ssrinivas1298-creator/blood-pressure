import pandas as pd
import os
import re

data_path = 'd:/blood presser/data.csv'

def analyze():
    if not os.path.exists(data_path):
        print("Data file not found")
        return

    # Read the data with separator detection
    try:
        df = pd.read_csv(data_path, encoding='utf-8-sig', sep=None, engine='python')
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Clean column names aggressively
    df.columns = [re.sub(r'[^a-zA-Z0-9 ]', '', str(c)).strip() for c in df.columns]
    print("Aggregate Columns:", df.columns.tolist())

    # Find relevant columns
    gender_col = next((c for c in df.columns if 'Gender' in c or 'Sex' in c), None)
    age_col = next((c for c in df.columns if 'Age' in c), None)
    param_col = next((c for c in df.columns if 'Blood pressure parameter' in c), None)
    char_col = next((c for c in df.columns if 'Characteristics' in c), None)
    value_col = next((c for c in df.columns if 'VALUE' in c), None)

    print(f"Detected: Gender={gender_col}, Age={age_col}, Param={param_col}, Char={char_col}, Value={value_col}")

    if param_col:
        print("Unique Blood pressure parameters:", df[param_col].unique().tolist())
    
    if char_col:
        print("Unique Characteristics:", df[char_col].unique().tolist())

    print("\nSample Data (First 15 rows):")
    cols_to_show = [c for c in [age_col, gender_col, param_col, char_col, value_col] if c]
    print(df[cols_to_show].head(15))

if __name__ == "__main__":
    analyze()
