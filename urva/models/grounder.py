from typing import Dict, Any, List
import torch
from torch import nn


from sentence_transformers import SentenceTransformer
import numpy as np

class FactGrounder:
    def __init__(self, cfg):
        self.sbert = SentenceTransformer('all-MiniLM-L6-v2')
        self.threshold = cfg.get("grounder", {}).get("threshold", 0.45)

    def compute_grounding(self, prediction: str, context: str) -> float:
        """G = α_lex * lexical_overlap + α_sem * semantic_sim"""
        # Lexical
        pred_tok = set(prediction.lower().split())
        ctx_tok = set(context.lower().split())
        lexical = len(pred_tok & ctx_tok) / max(len(ctx_tok), 1)
        # Semantic (SBERT)
        embs = self.sbert.encode([prediction, context])
        sem = float(np.dot(embs[0], embs[1]) / 
                    (np.linalg.norm(embs[0]) * np.linalg.norm(embs[1]) + 1e-8))
        sem = max(0.0, sem)  # clip negative
        
        return 0.5 * lexical + 0.5 * sem

    def __init__(self, cfg: Dict[str, Any]):
        super().__init__()
        hidden = cfg.get("hidden_size", 128)
        self.hidden = hidden
        self.encoder = nn.GRU(input_size=hidden, hidden_size=hidden, batch_first=True)
        self.scorer = nn.Linear(hidden, 1)
        self.threshold = cfg.get("grounder", {}).get("threshold", 0.45)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        if embeddings.size(1) == 0:
            return torch.zeros((embeddings.size(0), 0), device=embeddings.device)
        out, _ = self.encoder(embeddings)
        scores = torch.sigmoid(self.scorer(out)).squeeze(-1)
        return scores

    def _encode_tokens(self, tokens: List[int]) -> torch.Tensor:
        rng = torch.Generator()
        rng.manual_seed(sum(tokens) + len(tokens))
        device = self.encoder.weight_ih_l0.device
        return torch.randn(1, len(tokens), self.hidden, generator=rng, device=device)

    def ground_tokens(self, tokens: List[int]) -> Dict[str, Any]:
        if not tokens:
            return {"grounded_facts": [], "avg_score": 0.0}
        embeddings = self._encode_tokens(tokens)
        scores = self.forward(embeddings)[0]
        mask = scores > self.threshold
        grounded = [{"token": t, "score": float(s.detach())} for t, s, m in zip(tokens, scores, mask) if m]
        return {"grounded_facts": grounded, "avg_score": float(scores.mean().detach())}

    def __call__(self, batch: Dict[str, Any]) -> Dict[str, Any]:
        text = batch.get("text", "")
        tokens = [ord(c) % 97 for c in text]
        return self.ground_tokens(tokens)
