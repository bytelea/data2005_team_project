import pandas as pd

def analyze(df, top_n=20):
    # Analyzes dataset and return insights
    print("Running analyze...")
    
    results = {}

    # Top companies hiring
    result_df = df["company_name"].value_counts().head(top_n).reset_index()
    result_df.columns = ["company_name", "job_count"]

    # Top companies 
    top_companies = (
        df["company_name"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    top_companies.columns = ["company_name", "job_count"]
    results["top_companies"] = top_companies

    
    return result_df