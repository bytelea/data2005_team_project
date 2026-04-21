"""
tests/test_pipeline.py
----------------------
Unit tests for the loader, validator, and pipeline.

Run with:
    pytest tests/test_pipeline.py -v
"""

import json
import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from src.pipeline.loader import load_data, LoadError
from src.pipeline.validator import validate_data
from src.pipeline.pipeline import DataPipeline, PipelineError



# Helpers
VALID_RECORDS = [
    {
        "title": "Data Analyst",
        "company_name": "Acme Corp",
        "location": "Remote",
        "description": "Analyse data.",
        "salary_standardized": 80000,
    },
    {
        "title": "Senior Data Analyst",
        "company_name": "Globex",
        "location": "New York, NY",
        "description": "Lead analysis team.",
        "salary_standardized": 110000,
    },
]


def _write_csv(records: list[dict], path: Path) -> None:
    pd.DataFrame(records).to_csv(path, index=False)


def _write_json(records: list[dict], path: Path) -> None:
    with open(path, "w") as f:
        json.dump(records, f)



# Loader tests
class TestLoader:

    def test_load_csv(self, tmp_path):
        p = tmp_path / "jobs.csv"
        _write_csv(VALID_RECORDS, p)
        df = load_data(p)
        assert len(df) == 2
        assert "title" in df.columns

    def test_load_json(self, tmp_path):
        p = tmp_path / "jobs.json"
        _write_json(VALID_RECORDS, p)
        df = load_data(p)
        assert len(df) == 2
        assert "company_name" in df.columns

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(LoadError, match="File not found"):
            load_data(tmp_path / "nonexistent.csv")

    def test_unsupported_format_raises(self, tmp_path):
        p = tmp_path / "jobs.xlsx"
        p.write_text("dummy")
        with pytest.raises(LoadError, match="Unsupported format"):
            load_data(p)

    def test_empty_csv_raises(self, tmp_path):
        p = tmp_path / "empty.csv"
        p.write_text("")
        with pytest.raises(LoadError, match="no data"):
            load_data(p)



# Validator tests
class TestValidator:

    def test_valid_dataframe_passes(self):
        df = pd.DataFrame(VALID_RECORDS)
        report = validate_data(df)
        assert report.passed

    def test_missing_required_column(self):
        df = pd.DataFrame([{"title": "Analyst", "location": "Remote"}])
        report = validate_data(df)
        assert not report.passed
        assert any("company_name" in e for e in report.errors)

    def test_critical_null_is_error(self):
        records = VALID_RECORDS.copy()
        records[0] = dict(records[0], title=None)
        df = pd.DataFrame(records)
        report = validate_data(df)
        assert not report.passed
        assert any("title" in e for e in report.errors)

    def test_duplicate_rows_is_warning(self):
        df = pd.DataFrame(VALID_RECORDS * 2)  # double every row
        report = validate_data(df)
        assert report.passed  # duplicates are a warning, not an error
        assert any("duplicate" in w.lower() for w in report.warnings)

    def test_non_numeric_salary_is_warning(self):
        records = [dict(r, salary_standardized="unknown") for r in VALID_RECORDS]
        df = pd.DataFrame(records)
        report = validate_data(df)
        assert any("salary" in w.lower() for w in report.warnings)

    def test_high_null_rate_is_warning(self):
        df = pd.DataFrame(VALID_RECORDS)
        df["sparse_col"] = [None, None]  # 100% null
        report = validate_data(df)
        assert any("sparse_col" in w for w in report.warnings)



# Pipeline integration tests
class TestPipeline:

    def test_full_run_csv(self, tmp_path):
        p = tmp_path / "jobs.csv"
        _write_csv(VALID_RECORDS, p)
        pipeline = DataPipeline(verbose=False)
        df, report = pipeline.run(p)
        assert len(df) == 2
        assert report.passed

    def test_full_run_json(self, tmp_path):
        p = tmp_path / "jobs.json"
        _write_json(VALID_RECORDS, p)
        pipeline = DataPipeline(verbose=False)
        df, report = pipeline.run(p)
        assert len(df) == 2
        assert report.passed

    def test_strict_mode_raises_on_bad_data(self, tmp_path):
        p = tmp_path / "bad.csv"
        _write_csv([{"location": "Nowhere"}], p)  # missing required cols
        pipeline = DataPipeline(strict=True, verbose=False)
        with pytest.raises(PipelineError):
            pipeline.run(p)

    def test_non_strict_returns_df_despite_errors(self, tmp_path):
        p = tmp_path / "bad.csv"
        _write_csv([{"location": "Nowhere"}], p)
        pipeline = DataPipeline(strict=False, verbose=False)
        df, report = pipeline.run(p)
        assert not report.passed
        assert len(df) == 1
