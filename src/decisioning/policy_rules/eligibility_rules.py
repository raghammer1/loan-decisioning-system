import polars as pl
from decisioning.classes.PolicyRule import PolicyRule

def d1001() -> PolicyRule:
    """
    D1001: Check if age is 18 or older
    
    Returns a PolicyRule that checks if the applicant's age is 18 or older.
    """

    # D1001: Check if age is 18 or older
    rule_exprs:pl.Expr = pl.when(pl.col("age") >= 18) 
    rule_view:list[str] = ["application_id",'age']
    rule_description:str = "D1001: Check if age is 18 or older"
    rule_id = "D1001"

    return PolicyRule(rule_id, rule_description, rule_exprs, rule_view)