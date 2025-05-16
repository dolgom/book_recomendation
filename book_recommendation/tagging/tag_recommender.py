import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import torch


class TagRecommender:
    """태그 추천기 (Tag Recommender)"""

    def __init__(self, model, tags, pooling, cache_dir='cache'):

        self.model = model
        self.tags = tags
        self.pooling = pooling
        self.cache_path = os.path.join(cache_dir, "tag_embeddings.npy")

        if os.path.exists(self.cache_path):
            self.tag_embeddings = np.load(self.cache_path)
        else:
            tag_embeddings = self.model.encode(self.tags, return_all=True)
            pooled_tags = [self.pooling.mean_pooling(tag_emb) for tag_emb in tag_embeddings]
            self.tag_embeddings = torch.stack(pooled_tags).numpy()
            np.save(self.cache_path, self.tag_embeddings)

    def mean_recommend_tag(self, description):
        """평균 풀링 방식 태그 추천"""
        if not description.strip():
            return "태그 없음"

        sentences = description.split(". ")
        sentence_embeddings = self.model.encode(sentences, return_all=True)
        pooled = [self.pooling.mean_pooling(emb) for emb in sentence_embeddings]  # 3. 문장별 pooling
        description_embedding = torch.mean(torch.stack(pooled), dim=0)  # 4. 전체 평균 벡터

        cos_sim = cosine_similarity(description_embedding.unsqueeze(0).numpy(), self.tag_embeddings)
        best_tag_index = np.argmax(cos_sim)

        return self.tags[best_tag_index]

    def attention_recommend_tag(self, description):
        """self-attention 풀링 방식 태그 추천"""
        if not description.strip():
            return '태그 없음'

        sentences = description.split(". ")
        sentences_embeddings = self.model.encode(sentences, return_all=True)
        pooled = [self.pooling.self_attention_pooling(emb) for emb in sentences_embeddings]
        description_embedding = torch.mean(torch.stack(pooled), dim=0)

        cos_sim = cosine_similarity(description_embedding.reshape(1, -1), self.tag_embeddings)
        best_tag_index = np.argmax(cos_sim)

        return self.tags[best_tag_index]
