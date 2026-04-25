def export(df, results):
    import os

    os.makedirs("data/processed", exist_ok=True)

    # Save cleaned dataset
    df.to_csv("data/processed/cleaned_jobs.csv", index=False)
    print(f"[Exporter] Saved cleaned dataset ({len(df)} rows).")

    # If the results is a dictionary, save each
    if isinstance(results, dict):
        for key, value in results.items():
            if value is None:
                continue

            try:
                # DataFrame
                if hasattr(value, "to_csv"):
                    value.to_csv(f"data/processed/{key}.csv", index=False)

                # Series like top_jobs
                elif hasattr(value, "to_frame"):
                    value.to_frame().to_csv(f"data/processed/{key}.csv")

                # Dictionary like skill_counts
                elif isinstance(value, dict):
                    import pandas as pd
                    pd.DataFrame(list(value.items()), columns=["skill", "count"]) \
                        .to_csv(f"data/processed/{key}.csv", index=False)

                # Numbers 
                else:
                    with open(f"data/processed/{key}.txt", "w") as f:
                        f.write(str(value))

                print(f"[Exporter] Saved '{key}'")

            except Exception as e:
                print(f"[Exporter] Skipped '{key}': {e}")
