# Pipeline Builders
# DATA2005 Team Data Processing Project - [Web Data]

**Course:** DATA 2005 - Data-Centric Programming  
**Assessment:** Team Data Processing Project (20%)

## Team Members

| Name | Role | GitHub |
|------|------|--------|
| [Nada Abassi] | Data Engineer | [@nadaaa72] |
| [Monike Ozeias Santos] | Data Analyst | [@monikeoz] |
| [Hania Amear] | Visualization Lead | [@haniaamear25] |
| [Lea Stanisavljevic] | Documentation Lead | [@bytelea] |

## Project Description

This project analyses web-based job market data using a dataset of Data Analyst job postings collected from Google Search results. The aim is to explore trends in salaries, required skills, job locations and benefits. The project applies a full data processing pipeline including data loading, cleaning, transformation, analysis and visualisation using Python tools. The goal is to extract meaningful insights about the current demand in the data analyst job market.

## Dataset

- **Name:** Data Analyst Job Postings [Pay, Skills, Benefits]
- **Source:** https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search
- **Size:** ~10,000+ records
- **Format:** CSV

## Project Structure




## Data Analysis (Monike)

As the Data Analyst, I was responsible for extracting insights from the cleaned dataset using Pandas.

### Key Analysis Performed

- **Top Companies Hiring**
  - Identified companies with the highest number of job postings.
  - Example: Upwork, Talentify.io, and Walmart were among the top recruiters.

- **Top Job Locations**
  - Analyzed the most common job locations.
  - Found a high number of roles listed as "Anywhere" or "United States", indicating strong remote availability.

- **Top Job Titles**
  - Extracted the most frequent job roles.
  - "Data Analyst" and "Senior Data Analyst" were the most common positions.

- **Remote Work Analysis**
  - Calculated the percentage of remote jobs.
  - Result showed nearly all roles were remote (~100%).

- **Skill Demand Analysis**
  - Analyzed job descriptions to detect in-demand skills.
  - Most requested skills:
    - Excel
    - SQL
    - Python
    - Tableau
    - Power BI

### Tools & Techniques Used

- **Pandas** for data manipulation and analysis
- **Vectorised operations** (e.g. `value_counts()`, `.mean()`, `.sum()`)
- Feature extraction from text data (`str.contains()`)

### Output

The analysis results are:
- Displayed in the terminal
- Exported as CSV files for further use