import torch
from sentence_transformers import SentenceTransformer


class SBERTModel:
    """SBERT 모델로 임베딩벡터 구하기"""

    def __init__(self, model_name="jhgan/ko-sbert-sts", embedding_dim=768):
        self.model = SentenceTransformer(model_name)
        self.attention_layer = torch.nn.Linear(embedding_dim, 1, bias=False)  # 👈 self-attention용 레이어 정의

    # 문장 리스트를 SBERT 임베딩 벡터로 변환
    def encode(self, texts, return_all=False):
        if return_all:
            return self.model.encode(texts, convert_to_tensor=True, output_value='token_embeddings')
        return self.model.encode(texts, convert_to_tensor=True)
