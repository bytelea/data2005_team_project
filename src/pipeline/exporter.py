from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")


def export(df, results, output_dir=PROCESSED_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save the full cleaned dataset as a CSV file
    cleaned_path = output_dir / "cleaned_jobs.csv"
    df.to_csv(cleaned_path, index=False)
    print(f"[Exporter] Saved cleaned dataset to '{cleaned_path}' ({len(df):,} rows).")

    # Save each analysis result as its own CSV file
    for name, result_df in results.items():
        if result_df is None or result_df.empty:
            continue
        out_path = output_dir / f"{name}.csv"
        result_df.to_csv(out_path, index=False)
        print(f"[Exporter] Saved '{name}' to '{out_path}'.")
