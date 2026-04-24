import pandas as pd 

def clean_data(df):
    # Cleans the dataset by removing duplicates and missing values
    print("Running clean_data...")

    df = df.drop_duplicates()
    df = df.dropna()

    return df