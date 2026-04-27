import pandas as pd
import numpy as np

def analyze(df, top_n=20):
    # Analyzes dataset and return insights
    print("Running analyze...")

    def categorize_posted(text):
        if pd.isna(text):
            return None

        text = str(text).lower()

        if "hour" in text:
            return "last 24 hours"
        elif "day" in text:
            return "last 7 days"
        elif "week" in text:
            return "last month"
        elif "month" in text:
            return "older"
        else:
            return "other"

    df["posting_recency"] = df["posted_at"].apply(categorize_posted)

    recency_counts = df["posting_recency"].value_counts()

    print("\nPosting Recency:\n", recency_counts)

    # Top companies 
    top_companies = (
        df["company_name"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    top_companies.columns = ["company_name", "job_count"]

    # Top job titles
    top_jobs = (
        df["title"]
        .value_counts()
        .head(10)
    )
    print("\nTop Job Titles:\n", top_jobs)

    # Top locations
    top_locations = (
        df["location"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_locations.columns = ["location", "job_count"]
    print("\nTop Locations:\n", top_locations)

    # Remote job percentage 
    remote_percentage = None
    if "work_from_home" in df.columns:
        remote_percentage = df["work_from_home"].mean() * 100
        print(f"Remote jobs: {remote_percentage:.2f}%")

    # Skill demand (from features.py)
    skills = ["python", "sql", "excel", "tableau", "power bi"]
    skill_counts = {skill: df[skill].sum() for skill in skills if skill in df.columns}
    print("Skill demand:", skill_counts)

    # Average title length
    avg_title_length = np.mean(df["title"].str.len())
    print("Average job title length:", avg_title_length)

    # Average description length
    avg_description_length = df["description"].str.len().mean()
    print("Average description length:", avg_description_length)

    return {
    "top_companies": top_companies,
    "top_jobs": top_jobs,
    "top_locations": top_locations,
    "skill_counts": skill_counts,
    "remote_percentage": remote_percentage,
    "avg_title_length": avg_title_length,
    "avg_description_length": avg_description_length,
    "posting_recency": recency_counts,
    "total_jobs": len(df),
}