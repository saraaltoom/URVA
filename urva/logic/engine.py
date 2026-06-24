import json
from typing import Dict, List, Any
from .rules import LogicRules


class LogicEngine:
    """
    Expanded logic engine that checks multiple rule families and returns structured violations.
    """

    def __init__(self, rules: LogicRules):
        self.rules = rules

    @classmethod
    def from_file(cls, path: str) -> "LogicEngine":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        rules = LogicRules(**data)
        return cls(rules)

    def apply_rules(self, text: str, context: str = "", valid_labels: set = None) -> List[Dict]:
    results = []
    
    # Rule 1: Negation Conflict
    if self._has_negation_conflict(text):
        results.append({"rule": "Negation Conflict", "category": "LOGICAL", "r": 1})
    
    # Rule 2: Entity Mismatch
    if context and self._has_entity_mismatch(text, context):
        results.append({"rule": "Entity Mismatch", "category": "FACTUAL", "r": 1})
    
    # Rule 3: Numeric Inconsistency
    if self._has_numeric_inconsistency(text):
        results.append({"rule": "Numeric Inconsistency", "category": "NUMERIC", "r": 1})
    
    # Rule 4: Label Violation
    if valid_labels and self._has_label_violation(text, valid_labels):
        results.append({"rule": "Label Violation", "category": "LABEL", "r": 1})
    
    # Rule 5: Unsupported Assertion
    if context and self._has_unsupported_assertion(text, context):
        results.append({"rule": "Unsupported Assertion", "category": "GROUNDING", "r": 1})
    
    return results
        
        def compute_logic_penalty(self, text: str) -> float:
   
            N = 5  
            violations = self.apply_rules(text)
            triggered_rules = len({v["rule"] for v in violations})
            return min(1.0, triggered_rules / N)

    def check_statement(self, statement: str) -> List[Dict[str, Any]]:
        return self.apply_rules(statement)

    def summarize(self) -> str:
        return json.dumps(self.rules.__dict__, indent=2)
