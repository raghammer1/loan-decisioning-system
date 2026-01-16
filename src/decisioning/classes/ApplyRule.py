import polars as pl
from decisioning.classes.PolicyRule import PolicyRule


class ApplyRule:
    def __init__(self, policy_rule: PolicyRule, data_frame: pl.DataFrame):
        self.policy_rule: PolicyRule = policy_rule
        self.data_frame: pl.DataFrame = data_frame

    def execute_rule(self) -> pl.DataFrame:
        self.data_frame = self.data_frame.with_columns(
            pl.when(self.policy_rule.expressions)
            .then(pl.lit("Y"))
            .otherwise(pl.lit("N"))
            .alias(f"{self.policy_rule.rule_id}")
        )

        return self.data_frame
