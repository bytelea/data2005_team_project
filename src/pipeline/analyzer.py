import pandas as pd

def analyze(df, top_n=20):
    # Analyzes dataset n return insights
    print("Running analyze...")

    # Top companies hiring
    result_df = df["company_name"].value_counts().head(top_n).reset_index()
    result_df.columns = ["company_name", "job_count"]

    return result_df