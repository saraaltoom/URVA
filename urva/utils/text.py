from typing import List


def split_sentences(text: str) -> List[str]:
    parts = [p.strip() for p in text.replace("!", ".").replace("?", ".").split(".")]
    return [p for p in parts if p]

def compute_faithfulness(prediction: str, context: str) -> float:
    """
    F: token-level coverage — نسبة tokens السياق الموجودة في التنبؤ
    كما في الورقة: lexical coverage proxy
    """
    if not context or not prediction:
        return 0.0
    ctx_tokens = set(context.lower().split())
    pred_tokens = set(prediction.lower().split())
    if not ctx_tokens:
        return 0.0
    overlap = ctx_tokens.intersection(pred_tokens)
    return len(overlap) / len(ctx_tokens)
