import pandas as pd

def analyze(df, top_n=20):
    # Analyzes dataset and return insights
    print("Running analyze...")

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
    if "work_from_home" in df.columns:
        remote_percentage = df["work_from_home"].mean() * 100
        print(f"Remote jobs: {remote_percentage:.2f}%")

    # Skill demand (from features.py)
    skills = ["python", "sql", "excel", "tableau", "power bi"]
    skill_counts = {skill: df[skill].sum() for skill in skills if skill in df.columns}
    print("Skill demand:", skill_counts)

    return top_companies