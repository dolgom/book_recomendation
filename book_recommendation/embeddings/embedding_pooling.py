import torch


class EmbeddingPooling:
    def __init__(self, attention_layer):
        self.attention_layer = attention_layer

    # Mean pooling
    def mean_pooling(self, sentence_embeddings):
        if sentence_embeddings.size(0) > 0:
            return torch.mean(sentence_embeddings, dim=0)
        else:
            return torch.zeros(sentence_embeddings.size(1))

    # Self attention pooling
    def self_attention_pooling(self, sentence_embeddings):
        if sentence_embeddings.size(0) == 0:
            return torch.zeros(sentence_embeddings.size(1))

        scores = torch.tanh(self.attention_layer(sentence_embeddings)) # 중요도 계산
        weights = torch.softmax(scores, dim=0) # 정규화
        pooled = torch.sum(sentence_embeddings * weights, dim=0) # 가중합
        return pooled
