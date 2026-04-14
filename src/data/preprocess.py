import pandas as pd


def preprocess_data(df: pd.DataFrame, target_col: str = "Churn") -> pd.DataFrame:
    df = df.copy()

    # Remove leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    # Drop ID columns only if they exist
    cols_to_drop = ["customerID", "CustomerID", "customer_id"]
    existing_cols = [col for col in cols_to_drop if col in df.columns]
    if existing_cols:
        df = df.drop(columns=existing_cols)

    # Convert target to 0/1 if it is Yes/No text
    if target_col in df.columns and df[target_col].dtype == "object":
        df[target_col] = df[target_col].str.strip().map({"No": 0, "Yes": 1})

    # TotalCharges often has blanks in the dataset -> convert safely to numeric
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # SeniorCitizen should be 0/1 integers if present
    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].fillna(0).astype(int)

    # Fill numeric missing values with 0
    num_cols = df.select_dtypes(include=["number"]).columns
    df[num_cols] = df[num_cols].fillna(0)

    return df