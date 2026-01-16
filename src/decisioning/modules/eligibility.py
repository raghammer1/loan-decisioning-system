import polars as pl
from decisioning.classes.PolicyRule import PolicyRule
from decisioning.classes.ApplyRule import ApplyRule
from decisioning.policy_rules.eligibility_rules import d1001


def check_eligibility(pl_input_df: pl.DataFrame) -> pl.DataFrame:
    """
    Check eligibility of applicants based on predefined policy rules.
    Args:
        pl_input_df (pl.DataFrame): Input DataFrame containing applicant data.
    Returns:
        pl.DataFrame: DataFrame with eligibility results.
    """

    # *****************************************************
    # *********************** D1001 ***********************
    # *****************************************************
    """
    D1001: Check if age is 18 or older
    This rule checks if the applicant's age is 18 or older.
    If the condition is met, the rule marks the applicant as eligible ("Y"),
    otherwise as not eligible ("N").
    """

    eligibility_df: pl.DataFrame = ApplyRule(
        policy_rule=d1001(),
        data_frame=pl_input_df,
    ).execute_rule()

    # *****************************************************
    # *********************** D1002 ***********************
    # *****************************************************
    """
    D1002: Check if requested loan amount is within supported bounds
    This rule checks if the requested loan amount is between $1,000 and $50,000.
    If the condition is met, the rule marks the applicant as eligible ("Y"),
    otherwise as not eligible ("N").
    """

    # ********** END OF ELIGIBILITY POLICY RULES **********

    return eligibility_df
