import torch
from transformers import AutoModel, AutoTokenizer


# KoSimCSE 임베딩 모델
class KoSimCSEEmbedding:
    def __init__(self, model_name="BM-K/KoSimCSE-roberta", embedding_dim=768):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.attention_layer = torch.nn.Linear(embedding_dim, 1, bias=False)

    def encode(self, texts, return_all=False):
        with torch.no_grad():
            inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            outputs = self.model(**inputs)
            if return_all:
                return outputs.last_hidden_state
            return outputs.last_hidden_state[:, 0, :]  # CLS 토큰 사용
