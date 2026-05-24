"""
SIGAudit Basic Audit
Public-safe starter script for CSV data quality checks.

This script uses only local CSV files and fake/sample data.
It does not connect to private systems, databases, services or APIs.
"""

import argparse
from pathlib import Path

import pandas as pd


def load_rules(rules_path: str) -> pd.DataFrame:
    rules = pd.read_csv(rules_path).fillna("")
    required_columns = {"field", "required", "unique_key", "allowed_values"}
    missing = required_columns - set(rules.columns)
    if missing:
        raise ValueError(f"Rules file is missing columns: {sorted(missing)}")
    return rules


def field_completeness(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total = len(df)
    for field in df.columns:
        empty = df[field].isna() | (df[field].astype(str).str.strip() == "")
        empty_count = int(empty.sum())
        completeness = 100.0 if total == 0 else round((1 - empty_count / total) * 100, 2)
        rows.append({
            "field": field,
            "total_records": total,
            "empty_count": empty_count,
            "completeness_percent": completeness,
        })
    return pd.DataFrame(rows)


def required_field_violations(df: pd.DataFrame, rules: pd.DataFrame) -> pd.DataFrame:
    rows = []
    required_rules = rules[rules["required"].astype(str).str.lower().isin(["yes", "true", "1"])]
    for _, rule in required_rules.iterrows():
        field = rule["field"]
        if field not in df.columns:
            rows.append({"field": field, "issue": "required_field_missing_from_dataset", "row_number": "", "value": ""})
            continue
        mask = df[field].isna() | (df[field].astype(str).str.strip() == "")
        for idx, value in df.loc[mask, field].items():
            rows.append({"field": field, "issue": "required_value_empty", "row_number": int(idx) + 2, "value": value})
    return pd.DataFrame(rows)


def duplicate_key_violations(df: pd.DataFrame, rules: pd.DataFrame) -> pd.DataFrame:
    rows = []
    key_rules = rules[rules["unique_key"].astype(str).str.lower().isin(["yes", "true", "1"])]
    for _, rule in key_rules.iterrows():
        field = rule["field"]
        if field not in df.columns:
            rows.append({"field": field, "issue": "unique_key_missing_from_dataset", "row_number": "", "value": ""})
            continue
        duplicates = df[df[field].duplicated(keep=False) & df[field].notna()]
        for idx, value in duplicates[field].items():
            rows.append({"field": field, "issue": "duplicate_key", "row_number": int(idx) + 2, "value": value})
    return pd.DataFrame(rows)


def domain_violations(df: pd.DataFrame, rules: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, rule in rules.iterrows():
        field = rule["field"]
        allowed_raw = str(rule.get("allowed_values", "")).strip()
        if not allowed_raw:
            continue
        allowed = {item.strip() for item in allowed_raw.split("|") if item.strip()}
        if field not in df.columns:
            rows.append({"field": field, "issue": "domain_field_missing_from_dataset", "row_number": "", "value": "", "allowed_values": allowed_raw})
            continue
        values = df[field].astype(str).str.strip()
        mask = (values != "") & (~values.isin(allowed))
        for idx, value in values[mask].items():
            rows.append({"field": field, "issue": "value_outside_domain", "row_number": int(idx) + 2, "value": value, "allowed_values": allowed_raw})
    return pd.DataFrame(rows)


def write_report(df: pd.DataFrame, rules: pd.DataFrame, out_dir: str) -> None:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)

    completeness = field_completeness(df)
    required = required_field_violations(df, rules)
    duplicates = duplicate_key_violations(df, rules)
    domains = domain_violations(df, rules)

    completeness.to_csv(output / "field_completeness.csv", index=False)
    required.to_csv(output / "required_field_violations.csv", index=False)
    duplicates.to_csv(output / "duplicate_keys.csv", index=False)
    domains.to_csv(output / "domain_violations.csv", index=False)

    summary = pd.DataFrame([
        {"metric": "total_records", "value": len(df)},
        {"metric": "total_fields", "value": len(df.columns)},
        {"metric": "required_field_violations", "value": len(required)},
        {"metric": "duplicate_key_violations", "value": len(duplicates)},
        {"metric": "domain_violations", "value": len(domains)},
    ])
    summary.to_csv(output / "audit_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run basic SIGAudit CSV data quality checks.")
    parser.add_argument("--data", required=True, help="Path to CSV data file")
    parser.add_argument("--rules", required=True, help="Path to CSV validation rules")
    parser.add_argument("--out", default="output", help="Output folder")
    args = parser.parse_args()

    df = pd.read_csv(args.data).fillna("")
    rules = load_rules(args.rules)
    write_report(df, rules, args.out)
    print(f"Audit completed. Results written to: {args.out}")


if __name__ == "__main__":
    main()
