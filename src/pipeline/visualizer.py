from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#visual theme for all charst
sns.set_theme(style="whitegrid", palette="muted")

#directory for saving cahrts
CHARTS_DIR = Path("outputs/figures")


#to generate all vsiualizations
def visualize(results, output_dir=CHARTS_DIR):
    
    print("Running visualize...")
    #ensure directory exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    #individual charts
    plot_top_companies(results.get("top_companies"), output_dir)
    plot_top_jobs(results.get("top_jobs"), output_dir)
    plot_top_locations(results.get("top_locations"), output_dir)
    plot_skill_demand(results.get("skill_counts"), output_dir)
    plot_role_by_company(results.get("role_by_company"), output_dir)
    plot_skills_by_title(results.get("skills_by_title"), output_dir)
    
    print(f"Charts saved to: {output_dir}")

#to format and save charts
def save_chart(path):
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


#Chart 1: Top companies (vertical bar) 
# bar chart of top 10 companies by number of job postings
def plot_top_companies(df, output_dir):

    if df is None or df.empty:
        return
    #top 10 companies sort by job count
    top10 = df.head(10).sort_values("job_count", ascending=False)

    plt.figure(figsize=(10, 6))
    #create bar chart
    bars = plt.bar(top10["company_name"], top10["job_count"], color="steelblue")
    #value labels above bar
    for bar, val in zip(bars, top10["job_count"]):
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + top10["job_count"].max() * 0.01,
                 str(int(val)), ha="center", fontsize=8)

    #ttles adn labels
    plt.title("Top 10 Companies by Number of Job Postings")
    plt.xlabel("Company")
    plt.ylabel("Number of Postings")
    plt.xticks(rotation=30, ha="right")

    save_chart(output_dir / "top_companies.png")


# Chart 2: Top job titles (lollipop)
#lollipop chart of top job titles by frequency
def plot_top_jobs(top_jobs, output_dir):

    if top_jobs is None or top_jobs.empty:
        return
    #reste indexand rename colums
    df = top_jobs.reset_index()
    df.columns = ["title", "count"]
    df = df.sort_values("count")

    plt.figure(figsize=(10, 6))
    #horizontal lines for lollipop stick
    plt.hlines(df["title"], 0, df["count"], linewidth=2, color="steelblue")
    #cirlces at the end
    plt.plot(df["count"], df["title"], "o", color="steelblue", markersize=8)

    #value labe;s
    for _, row in df.iterrows():
        plt.text(row["count"] + df["count"].max() * 0.01, row["title"],
                 str(int(row["count"])), va="center", fontsize=8)
        
    #titles and labels
    plt.title("Top 10 Job Titles")
    plt.xlabel("Number of Postings")
    plt.ylabel("Job Title")
    plt.xlim(0, df["count"].max() * 1.15)

    save_chart(output_dir / "top_job_titles.png")


#Chart 3: Top locations with average line 
#bar chart of top job locations, highlighting location above avg of posting
def plot_top_locations(df, output_dir):

    if df is None or df.empty:
        return
    #   slect top 10 locations
    df = df.head(10).copy()
    #average job ocunt
    avg = df["job_count"].mean()

    plt.figure(figsize=(10, 6))
    #Bar chart
    bars = plt.bar(df["location"], df["job_count"], color="steelblue")
    #average line
    plt.axhline(
        avg, color="red", linestyle="--", linewidth=1.2, label=f"Average ({avg:.0f})")

    #highlight bars above avg
    for bar, val in zip(bars, df["job_count"]):
        if val >= avg:
            bar.set_color("darkorange")
    #titels and labels
    plt.title("Top 10 Job Locations (orange = above average)")
    plt.xlabel("Location")
    plt.ylabel("Number of Postings")
    plt.xticks(rotation=30, ha="right")#rotate labels
    plt.legend() #legend

    save_chart(output_dir / "top_locations.png")


#Chart 4: Skill demand (bar + donut 
# combined visualisation of skill demnad
def plot_skill_demand(skill_counts, output_dir):
    if not skill_counts:
        return
    #convert dict to Dataframe to easily manipulate
    df = pd.DataFrame(list(skill_counts.items()), columns=["skill", "count"])
    #sort skills by demand
    df = df.sort_values("count", ascending=False)
    total = df["count"].sum()
    df["percentage"] = df["count"] / total * 100
    #2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: bar chart
    #titels adn labels
    axes[0].bar(df["skill"].str.title(), df["count"], color="steelblue")
    axes[0].set_title("Skill Demand (Count)")
    axes[0].set_xlabel("Skill")
    axes[0].set_ylabel("Number of Postings")
    
    #value labels over bars
    for i, val in enumerate(df["count"]):
        axes[0].text(i, val + 10, str(int(val)), ha="center", fontsize=9)

    # Right: donut chart
    wedges, texts, autotexts = axes[1].pie(
        df["percentage"], #percentages
        labels=df["skill"].str.title(), #skill labels
        autopct="%1.1f%%", # show %
        startangle=140, #rotate
        wedgeprops={"width": 0.5}   #donut chart
    )
    #titele for donut
    axes[1].set_title("Skill Demand (% Share)")
    
    #main title
    plt.suptitle("In-Demand Skills Across Job Postings", fontsize=13, fontweight="bold")

    save_chart(output_dir / "skill_demand.png")

# Chart 5: Top companies hiring for each role (stacekd bar chart)
# Shows which companies dominate specific job titles
#Each company is normalised to 100% so that role proportions
# can be compared fairly between companies regardless of size.
def plot_role_by_company(role_by_company, output_dir):
    #missing empty data check
    if role_by_company is None or role_by_company.empty:
        return
    #copy to not modify orginal dataset
    df = role_by_company.copy()

    # Convered to % so each company = 100%
    df_pct = df.div(df.sum(axis=1), axis=0) * 100

    #  top 5 companies 
    top_companies = df.sum(axis=1).sort_values(ascending=False).head(5).index
    #filter to only have top companies
    df_pct = df_pct.loc[top_companies]

    # Plot stacked bar
    df_pct.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="tab10")

#labels and titles
    plt.title("Role Distribution by Company (%)")
    plt.xlabel("Company")
    plt.ylabel("Percentage of Job Roles")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Job Title", bbox_to_anchor=(1.01, 1))

    save_chart(output_dir / "role_by_company_stacked.png")

# Chart 6: Skill demand by job title (heatmap)
#heatmap showing which skills are most demanded for each top job title
def plot_skills_by_title(skills_by_title, output_dir):
    if skills_by_title is None or skills_by_title.empty:
        return

    df = skills_by_title.copy()
    df.columns = [c.title() for c in df.columns]

    # Convert counts to percentage per job title
    df_pct = df.div(df.sum(axis=1), axis=0) * 100

    plt.figure(figsize=(10, 6))
    sns.heatmap(df_pct, annot=True, cmap="YlGnBu", fmt=".1f")

    plt.title("Skill Demand by Job Title (%)")
    plt.xlabel("Skill")
    plt.ylabel("Job Title")

    save_chart(output_dir / "skills_by_title_heatmap.png")