class PolicyRule:
    def __init__(self, rule_id: str, description: str, expressions, view: list[str]):
        self.rule_id = rule_id
        self.description = description
        self.expressions = expressions
        self.view = view
