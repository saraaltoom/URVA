import re
import json
from typing import List, Dict, Any

try:
    import spacy
    _nlp = spacy.load("en_core_web_sm")
    _SPACY_AVAILABLE = True
except Exception:
    _nlp = None
    _SPACY_AVAILABLE = False


class LogicEngine:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    @classmethod
    def from_file(cls, path: str) -> "LogicEngine":
        with open(path, "r", encoding="utf-8") as f:
            rules = json.load(f)
        return cls(rules)

    def check_statement(self, text: str) -> List[Dict[str, Any]]:
        return self.apply_rules(text)

    doc = _nlp(text) if _SPACY_AVAILABLE and _nlp else None

    

    def apply_rules(self, text: str) -> List[Dict[str, Any]]:
    violations = []
    text_lower = text.lower()
    doc = _nlp(text) if _SPACY_AVAILABLE and _nlp else None

    # Rule 1: Negation Conflict (SpaCy-based)
    if doc:
        has_neg = any(tok.dep_ == "neg" for tok in doc)
        has_aff = any(tok.pos_ == "VERB" and tok.dep_ != "neg" for tok in doc)
        if has_neg and has_aff:
            violations.append({
                "rule": "NegationConflict",
                "category": "LOGICAL",
                "detail": "Negation detected via dependency parse"
            })
    else:
        neg_patterns = [
            (r"\bis\b", r"\bis not\b"),
            (r"\bwas\b", r"\bwas not\b"),
            (r"\bcan\b", r"\bcannot\b"),
        ]
        for pos, neg in neg_patterns:
            if re.search(pos, text_lower) and re.search(neg, text_lower):
                violations.append({
                    "rule": "NegationConflict",
                    "category": "LOGICAL",
                    "detail": "Affirmative and negated claims coexist"
                })
                break

    # Rule 2: Entity Mismatch (SpaCy NER)
    if doc:
        entities = [ent.text for ent in doc.ents]
    else:
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)
    if len(entities) != len(set(entities)):
        seen = {}
        for e in entities:
            seen[e] = seen.get(e, 0) + 1
        if any(v > 2 for v in seen.values()):
            violations.append({
                "rule": "EntityMismatch",
                "category": "FACTUAL",
                "detail": "Repeated conflicting entity references"
            })

        # Rule 3: Numeric Inconsistency
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        if len(numbers) >= 2:
            nums = [float(n) for n in numbers]
            if max(nums) > 10 * min(nums) and min(nums) > 0:
                violations.append({
                    "rule": "NumericInconsistency",
                    "category": "NUMERIC",
                    "detail": f"Suspicious numeric range: {min(nums)} vs {max(nums)}"
                })

        # Rule 4: Label Violation
        valid_labels = {"supports", "refutes", "not enough info",
                        "hallucinated", "supported", "yes", "no"}
        tokens = set(text_lower.split())
        label_tokens = tokens & valid_labels
        if len(label_tokens) > 1:
            violations.append({
                "rule": "LabelViolation",
                "category": "LOGICAL",
                "detail": f"Multiple conflicting labels: {label_tokens}"
            })

        # Rule 5: Unsupported Assertion
        assertion_markers = ["definitely", "certainly", "always", "never",
                             "impossible", "guaranteed", "proven"]
        found = [m for m in assertion_markers if m in text_lower]
        if found:
            violations.append({
                "rule": "UnsupportedAssertion",
                "category": "FACTUAL",
                "detail": f"Strong unsupported assertion markers: {found}"
            })

        return violations
