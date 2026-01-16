import polars as pl
from decisioning.classes.PolicyRule import PolicyRule


class ApplyRule:
    def __init__(self, policy_rule: PolicyRule, data_frame: pl.DataFrame):
        self.policy_rule: PolicyRule = policy_rule
        self.data_frame: pl.DataFrame = data_frame

    def execute_rule(self) -> pl.DataFrame:
        for expression in self.policy_rule.expressions:
            self.data_frame = expression(self.data_frame)

        return self.data_frame
