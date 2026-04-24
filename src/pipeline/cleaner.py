import pandas as pd 

def clean_data(df):
    # Cleans the dataset by removing duplicates and missing values
    print("Running clean_data...")

    # Remove duplicates
    df = df.drop_duplicates()

    # Drop rows missing key job information
    essential_columns = ['title', 'company_name', 'location']
    df = df.dropna(subset=essential_columns)

    # Clean text
    df["title"] = df["title"].str.strip()
    df["company_name"] = df["company_name"].str.strip()

    # Drop useless columns 
    df = df.drop(columns=[
        "thumbnail", "job_id", "Unanamed: 0"
    ], errors="ignore")

    return df