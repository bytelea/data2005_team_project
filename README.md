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

As the Data Analyst, I was responsible for extracting meaningful insights from the cleaned dataset using Python, primarily with Pandas and NumPy.

### Key Analysis Performed

- **Top Companies Hiring**
  - Identified companies with the highest number of job postings using frequency analysis.
  - Example: Upwork, Talentify.io, and Walmart were among the top recruiters.

- **Top Job Locations**
  - Analyzed the most common job locations across the dataset.
  - A large proportion of roles were listed as "Anywhere" or "United States", indicating a strong presence of remote or broadly available positions.

- **Top Job Titles**
  - Extracted the most frequent job roles using value counts.
  - "Data Analyst" and "Senior Data Analyst" were the most common roles, followed by related positions such as Data Scientist and Business Data Analyst.

- **Remote Work Analysis**
  - Calculated the percentage of remote jobs using the `work_from_home` column.
  - Results indicated that nearly all jobs in the dataset were remote (~100%).

- **Skill Demand Analysis**
  - Performed feature extraction on job descriptions to detect in-demand technical skills.
  - Created new columns for skills such as Python, SQL, Excel, Tableau, and Power BI.
  - Analysis showed that Excel and SQL were the most frequently requested skills, followed by Python, Tableau, and Power BI.

- **Statistical Insight**
  - Used NumPy to compute summary statistics, such as the average job title length, demonstrating additional numerical analysis on the dataset.

### Tools & Techniques Used

- **Pandas** for data manipulation, aggregation, and analysis
- **NumPy** for statistical computations
- **Vectorised operations** (e.g. `value_counts()`, `.mean()`, `.sum()`) for efficient processing
- **Text-based feature extraction** using `str.contains()` to analyse unstructured job descriptions

### Output

The analysis results are:
- Displayed in the terminal during pipeline execution
- Exported as CSV files for further use in visualization and reporting