import pandas as pd

REQUIRED_COLUMNS = ["title", "company_name", "location", "description"]
CRITICAL_COLUMNS = ["title", "company_name"]
SALARY_COLUMNS = ["salary_standardized", "salary_avg", "salary_min", "salary_max"]


class ValidationReport:
    def __init__(self):
        self.errors = []
        self.warnings = []

    @property
    def passed(self):
        # The report passes only if there are no errors
        return len(self.errors) == 0

    def summary(self):
        lines = ["=== Validation Report ==="]

        if self.passed:
            lines.append("Status: PASSED")
        else:
            lines.append("Status: FAILED")

        if self.errors:
            lines.append(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  [ERROR] {error}")

        if self.warnings:
            lines.append(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  [WARN]  {warning}")

        if not self.errors and not self.warnings:
            lines.append("No issues found.")

        return "\n".join(lines)

    def __repr__(self):
        return self.summary()


def validate_data(df):
    report = ValidationReport()

    # Make a lowercase version of column names for easier comparison
    lower_cols = {col.lower(): col for col in df.columns}

    # Check that all required columns exist
    for col in REQUIRED_COLUMNS:
        if col.lower() not in lower_cols:
            report.errors.append(f"Missing required column: '{col}'")

    # Check that the dataset has at least one row
    if len(df) == 0:
        report.errors.append("The dataset has 0 rows.")

    # Stop here if there are already errors
    if not report.passed:
        return report

    # Check that critical columns have no empty values
    for col in CRITICAL_COLUMNS:
        actual = lower_cols.get(col.lower())
        if actual:
            null_count = df[actual].isna().sum()
            if null_count > 0:
                pct = null_count / len(df)
                report.errors.append(
                    f"Column '{actual}' has {null_count} missing values ({pct:.1%} of rows)."
                )

    # Warn if a column is more than 50% empty
    for col in df.columns:
        rate = df[col].isna().mean()
        if rate > 0.50:
            report.warnings.append(f"Column '{col}' is {rate:.1%} empty.")

    # Warn if there are duplicate rows
    n_dupes = df.duplicated().sum()
    if n_dupes > 0:
        report.warnings.append(f"{n_dupes} duplicate row(s) found.")

    # Warn if salary columns contain non-numeric values
    for col in SALARY_COLUMNS:
        actual = lower_cols.get(col.lower())
        if actual is None:
            continue
        non_null = df[actual].dropna()
        if len(non_null) == 0:
            continue
        non_numeric = pd.to_numeric(non_null, errors="coerce").isna().sum()
        if non_numeric > 0:
            report.warnings.append(
                f"Salary column '{actual}' has {non_numeric} non-numeric value(s)."
            )

    return report
