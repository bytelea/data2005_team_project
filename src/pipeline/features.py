import pandas as pd

def extract_features(df):
    # Extracts useful features from job descriptions
    print("Running extract_features...")

    # Make sure description exists
    df["description"] = df["description"].fillna("").str.lower()

    # List of skills to detect
    skills = ["python", "sql", "excel", "tableau", "power bi"]

    # Create new columns for each skill
    for skill in skills:
        df[skill] = df["description"].str.contains(skill, na=False)

    return df