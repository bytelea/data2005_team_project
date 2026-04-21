# =============================================================================
# pipeline.py — Data Engineer (Pipeline Architecture)
# =============================================================================
# This file is the main entry point for the project.
# It connects every team member's module together and runs them in order.
#
# Team module responsibilities:
#   Data Engineer      → loader.py, validator.py, exporter.py, pipeline.py
#   Data Analyst       → cleaner.py, features.py, analyzer.py
#   Visualization Lead → visualizer.py
# =============================================================================

#Data Engineer imports (loader, validator, exporter) 
from .loader import load_data, LoadError
from .validator import validate_data
from .exporter import export

#Data Analyst imports (cleaner, features, analyzer) 
from .cleaner import clean_data
from .features import extract_features
from .analyzer import analyze

#Visualization Lead imports (visualizer) 
from .visualizer import visualize


class PipelineError(Exception):
    pass


class DataPipeline:
    def __init__(self, strict=True, verbose=True, top_n=20, charts=True):
        self.strict = strict    # If True, stop the pipeline when validation fails
        self.verbose = verbose  # If True, print the full validation report
        self.top_n = top_n      # How many top results to keep in charts/tables
        self.charts = charts    # If True, save charts as image files

    def run(self, filepath):
        print("\n" + "=" * 60)
        print(" DATA PIPELINE STARTING")
        print("=" * 60)

        
        # STEP 1 - Load data  (Data Engineer)
        # Reads the CSV or JSON file into a table using loader.py
        print("\n[Step 1/6] Loading data...")
        df = load_data(filepath)
        print(f"           {len(df):,} rows x {len(df.columns)} columns loaded.")

       
        # STEP 2 - Validate data  (Data Engineer)
        # Checks for missing columns, empty values, duplicates using validator.py
        print("\n[Step 2/6] Validating...")
        report = validate_data(df)
        if self.verbose:
            print(report.summary())
        if not report.passed and self.strict:
            raise PipelineError("Validation failed. Fix errors before continuing.\n" + report.summary())

        
        # STEP 3 - Clean data  (Data Analyst)
        # Removes duplicates, fills missing values, parses skills using cleaner.py
        print("\n[Step 3/6] Cleaning...")
        df = clean_data(df)
        print(f"           {len(df):,} rows after cleaning.")

       
        # STEP 4 - Extract features  (Data Analyst)
        # Adds year, month, city, state, seniority columns using features.py
        print("\n[Step 4/6] Extracting features...")
        df = extract_features(df)

        
        # STEP 5 - Analyse trends  (Data Analyst)
        # Calculates top skills, salaries, job counts using analyzer.py
        print("\n[Step 5/6] Analysing trends...")
        results = analyze(df, top_n=self.top_n)

        
        # STEP 6 - Visualise and export  (Visualization Lead + Data Engineer)
        # Saves charts using visualizer.py, saves CSV files using exporter.py
        print("\n[Step 6/6] Saving charts and files...")
        if self.charts:
            try:
                visualize(results)
            except ImportError:
                print("[Visualizer] matplotlib/seaborn not installed — skipping charts.")
        export(df, results)

        print("\n" + "=" * 60)
        print(" PIPELINE COMPLETE")
        print("=" * 60 + "\n")

        return df, results
