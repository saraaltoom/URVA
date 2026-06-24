from typing import Dict, Any, List
import torch
from torch import nn
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    _SBERT_AVAILABLE = True
except ImportError:
    _SBERT_AVAILABLE = False


class FactGrounder(nn.Module):
    def __init__(self, cfg: Dict[str, Any]):
        super().__init__()
        self.hidden = cfg.get("hidden_size", 128)
        self.threshold = cfg.get("grounder", {}).get("threshold", 0.45)
        self.encoder = nn.GRU(input_size=self.hidden, hidden_size=self.hidden, batch_first=True)
        self.scorer = nn.Linear(self.hidden, 1)
        # SBERT for semantic grounding (paper Section II-C)
        self.sbert = SentenceTransformer('all-MiniLM-L6-v2') if _SBERT_AVAILABLE else None

    def compute_grounding(self, prediction: str, context: str) -> float:
        """Hybrid grounding G = 0.5*lexical + 0.5*semantic (paper Eq. αF+βG)"""
        pred_tok = set(prediction.lower().split())
        ctx_tok = set(context.lower().split())
        lexical = len(pred_tok & ctx_tok) / max(len(ctx_tok), 1)
        if self.sbert:
            embs = self.sbert.encode([prediction, context])
            sem = float(np.dot(embs[0], embs[1]) /
                        (np.linalg.norm(embs[0]) * np.linalg.norm(embs[1]) + 1e-8))
            sem = max(0.0, sem)
        else:
            sem = lexical  
        return 0.5 * lexical + 0.5 * sem

    def _encode_tokens(self, tokens: List[int]) -> torch.Tensor:
        rng = torch.Generator()
        rng.manual_seed(sum(tokens) + len(tokens))
        device = self.encoder.weight_ih_l0.device
        return torch.randn(1, len(tokens), self.hidden, generator=rng, device=device)

    def ground_tokens(self, tokens: List[int]) -> Dict[str, Any]:
        if not tokens:
            return {"grounded_facts": [], "avg_score": 0.0}
        embeddings = self._encode_tokens(tokens)
        out, _ = self.encoder(embeddings)
        scores = torch.sigmoid(self.scorer(out)).squeeze(-1)[0]
        mask = scores > self.threshold
        grounded = [{"token": t, "score": float(s.detach())}
                    for t, s, m in zip(tokens, scores, mask) if m]
        return {"grounded_facts": grounded, "avg_score": float(scores.mean().detach())}

    def __call__(self, batch: Dict[str, Any]) -> Dict[str, Any]:
        text = batch.get("text", "")
        tokens = [ord(c) % 97 for c in text]
        return self.ground_tokens(tokens)
