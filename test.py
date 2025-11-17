# test.py
import pandas as pd
from pathlib import Path
from send_email import send_email

def run_data_cleaning(csv_path: str = "financial_risk_assessment.csv") -> bool:
    """Clean the financial risk assessment dataset."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path.resolve()}")

    # Load the dataset
    df = pd.read_csv(csv_path)

    # --- Example cleaning steps ---
    # 1. Drop duplicate rows
    df = df.drop_duplicates()

    # 2. Handle missing values
    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    df[numeric_cols] = df[numeric_cols].fillna(0)
    df[categorical_cols] = df[categorical_cols].fillna("Unknown")

    # 3. Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # 4. Example: ensure "amount" column is numeric
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    # 5. Save cleaned dataset
    out_path = csv_path.with_name(f"{csv_path.stem}_cleaned{csv_path.suffix}")
    df.to_csv(out_path, index=False)

    return True


if __name__ == "__main__":
    # Adjust recipients as needed
    recipient = "faris.zaimir@bnm.gov.my"
    cc = None  # e.g., "dr.ho@bnm.gov.my;dr.tng@bnm.gov.my"

    try:
        success = run_data_cleaning("financial_risk_assessment.csv")
        if success:
            subject = "Data Cleaning Status"
            body = (
                "Hi Data Analyst Team,\n\n"
                "All processes executed successfully ✅\n\n"
                "Output: financial_risk_assessment_cleaned.csv\n\n"
                "Regards,\nAutomation Bot"
            )
        else:
            subject = "Data Cleaning Status"
            body = (
                "Hi Data Analyst Team,\n\n"
                "Processes did not execute as expected ❌\n\n"
                "Regards,\nAutomation Bot"
            )

        send_email(subject=subject, recipient=recipient, body_text=body, cc=cc)

    except Exception as e:
        subject = "Data Cleaning Status"
        body = (
            "Hi Data Analyst Team,\n\n"
            f"Process failed with error: {e}\n\n"
            "Regards,\nAutomation Bot"
        )
        # even on error, we try to notify
        send_email(subject=subject, recipient=recipient, body_text=body, cc=cc)
        # re-raise if you want the script to fail for schedulers/monitoring
        # raise