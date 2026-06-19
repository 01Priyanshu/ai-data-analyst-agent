"""
Data Loader & Profiler Module
Handles CSV loading, data profiling, and SQLite database creation.
"""

import pandas as pd
import sqlite3
import os
import json


class DataLoader:
    """Loads CSV files, profiles them, and creates an in-memory SQLite database."""

    def __init__(self):
        self.df = None
        self.db_conn = None
        self.table_name = "data"
        self.file_name = None

    def load_csv(self, file_path: str) -> dict:
        """Load a CSV file and return a data profile summary."""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            self.df = pd.read_csv(file_path)
            self.file_name = os.path.basename(file_path)

            # Create SQLite in-memory database
            self.db_conn = sqlite3.connect(":memory:")
            self.df.to_sql(self.table_name, self.db_conn, index=False, if_exists="replace")

            return self.get_profile()
        except Exception as e:
            return {"error": f"Failed to load CSV: {str(e)}"}

    def get_profile(self) -> dict:
        """Generate a comprehensive data profile."""
        if self.df is None:
            return {"error": "No data loaded. Please load a CSV file first."}

        profile = {
            "file_name": self.file_name,
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "column_details": [],
            "memory_usage": f"{self.df.memory_usage(deep=True).sum() / 1024:.1f} KB",
            "missing_values": int(self.df.isnull().sum().sum()),
            "duplicate_rows": int(self.df.duplicated().sum()),
        }

        for col in self.df.columns:
            col_info = {
                "name": col,
                "dtype": str(self.df[col].dtype),
                "non_null": int(self.df[col].notna().sum()),
                "null_count": int(self.df[col].isnull().sum()),
                "unique_values": int(self.df[col].nunique()),
            }

            # Add stats for numeric columns
            if pd.api.types.is_numeric_dtype(self.df[col]):
                col_info["min"] = float(self.df[col].min())
                col_info["max"] = float(self.df[col].max())
                col_info["mean"] = round(float(self.df[col].mean()), 2)
                col_info["median"] = float(self.df[col].median())
                col_info["std"] = round(float(self.df[col].std()), 2)

            # Add top values for categorical columns
            if self.df[col].dtype == "object" or self.df[col].nunique() < 15:
                top_values = self.df[col].value_counts().head(5).to_dict()
                col_info["top_values"] = {str(k): int(v) for k, v in top_values.items()}

            profile["column_details"].append(col_info)

        return profile

    def run_sql(self, query: str) -> dict:
        """Execute a SQL query against the loaded data."""
        if self.db_conn is None:
            return {"error": "No data loaded. Please load a CSV file first."}

        try:
            result_df = pd.read_sql_query(query, self.db_conn)
            return {
                "success": True,
                "query": query,
                "rows_returned": len(result_df),
                "columns": list(result_df.columns),
                "data": result_df.to_dict(orient="records"),
                "preview": result_df.to_string(index=False, max_rows=20),
            }
        except Exception as e:
            return {"error": f"SQL Error: {str(e)}", "query": query}

    def get_sample(self, n: int = 5) -> str:
        """Return a sample of the data as a formatted string."""
        if self.df is None:
            return "No data loaded."
        return self.df.head(n).to_string(index=False)

    def get_schema(self) -> str:
        """Return the SQL schema of the table."""
        if self.df is None:
            return "No data loaded."

        schema_lines = [f"TABLE: {self.table_name}", "COLUMNS:"]
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            sql_type = "TEXT"
            if "int" in dtype:
                sql_type = "INTEGER"
            elif "float" in dtype:
                sql_type = "REAL"
            schema_lines.append(f"  - {col} ({sql_type})")

        return "\n".join(schema_lines)
