import pandas as pd
import great_expectations as gx
from typing import Tuple, List


def validate_telco_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Comprehensive data validation for Telco Customer Churn dataset
    using Great Expectations (modern GX Core API).

    Returns:
        Tuple[bool, List[str]]:
            - success: True if all checks pass
            - failed_expectations: list of failed expectation names
    """

    print("🔍 Starting data validation with Great Expectations...")

    # ------------------------------------------------------------------
    # 0) Defensive copy
    # ------------------------------------------------------------------
    df = df.copy()

    # ------------------------------------------------------------------
    # 1) Preprocessing for known Telco issues
    # ------------------------------------------------------------------
    # TotalCharges often comes as string and may contain blank values.
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # ------------------------------------------------------------------
    # 2) Create GX context and batch from dataframe
    # ------------------------------------------------------------------
    context = gx.get_context()

    datasource_name = "telco_pandas_ds"
    asset_name = "telco_dataframe_asset"
    batch_definition_name = "telco_whole_dataframe_batch"

    # Reuse datasource if it already exists
    try:
        data_source = context.data_sources.get(datasource_name)
    except Exception:
        data_source = context.data_sources.add_pandas(datasource_name)

    # Reuse asset if it already exists
    try:
        data_asset = data_source.get_asset(asset_name)
    except Exception:
        data_asset = data_source.add_dataframe_asset(name=asset_name)

    # Reuse batch definition if it already exists
    try:
        batch_definition = data_asset.get_batch_definition(batch_definition_name)
    except Exception:
        batch_definition = data_asset.add_batch_definition_whole_dataframe(
            batch_definition_name
        )

    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": df}
    )

    # ------------------------------------------------------------------
    # 3) Define expectations
    # ------------------------------------------------------------------
    expectations = [
        # =========================
        # SCHEMA VALIDATION
        # =========================
        gx.expectations.ExpectColumnToExist(column="customerID"),
        gx.expectations.ExpectColumnValuesToNotBeNull(column="customerID"),

        gx.expectations.ExpectColumnToExist(column="gender"),
        gx.expectations.ExpectColumnToExist(column="Partner"),
        gx.expectations.ExpectColumnToExist(column="Dependents"),

        gx.expectations.ExpectColumnToExist(column="PhoneService"),
        gx.expectations.ExpectColumnToExist(column="InternetService"),
        gx.expectations.ExpectColumnToExist(column="Contract"),

        gx.expectations.ExpectColumnToExist(column="tenure"),
        gx.expectations.ExpectColumnToExist(column="MonthlyCharges"),
        gx.expectations.ExpectColumnToExist(column="TotalCharges"),

        # =========================
        # BUSINESS LOGIC VALIDATION
        # =========================
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="gender",
            value_set=["Male", "Female"]
        ),
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Partner",
            value_set=["Yes", "No"]
        ),
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Dependents",
            value_set=["Yes", "No"]
        ),
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="PhoneService",
            value_set=["Yes", "No"]
        ),
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Contract",
            value_set=["Month-to-month", "One year", "Two year"]
        ),
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="InternetService",
            value_set=["DSL", "Fiber optic", "No"]
        ),

        # =========================
        # NUMERIC RANGE VALIDATION
        # =========================
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="tenure",
            min_value=0,
            max_value=120
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(column="tenure"),

        gx.expectations.ExpectColumnValuesToBeBetween(
            column="MonthlyCharges",
            min_value=0,
            max_value=200
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(column="MonthlyCharges"),

        # TotalCharges may contain NaN after conversion from blank strings
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="TotalCharges",
            min_value=0
        ),

        # Allow a tiny fraction of nulls due to known Telco dataset blanks
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="TotalCharges",
            mostly=0.99
        ),

        # =========================
        # DATA CONSISTENCY CHECKS
        # =========================
        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
            column_A="TotalCharges",
            column_B="MonthlyCharges",
            or_equal=True,
            mostly=0.95
        ),
    ]

    # ------------------------------------------------------------------
    # 4) Run validation suite
    # ------------------------------------------------------------------
    print("   ⚙️ Running validation suite...")
    results = []

    for expectation in expectations:
        result = batch.validate(expectation)
        results.append(result)

    # ------------------------------------------------------------------
    # 5) Process results
    # ------------------------------------------------------------------
    failed_expectations = []

    for r in results:
        if not r.success:
            try:
                failed_expectations.append(r.expectation_config.type)
            except Exception:
                failed_expectations.append("unknown_expectation")

    total_checks = len(results)
    passed_checks = sum(1 for r in results if r.success)
    failed_checks = total_checks - passed_checks
    success = failed_checks == 0

    # ------------------------------------------------------------------
    # 6) Print summary
    # ------------------------------------------------------------------
    if success:
        print(f"✅ Data validation PASSED: {passed_checks}/{total_checks} checks successful")
    else:
        print(f"❌ Data validation FAILED: {failed_checks}/{total_checks} checks failed")
        print(f"   Failed expectations: {failed_expectations}")

    return success, failed_expectations