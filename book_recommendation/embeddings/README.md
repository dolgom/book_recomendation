# 📦 Embedding Module

다양한 문장 임베딩 모델과 임베딩 벡터를 처리하는 **풀링(pooling)** 전략을 포함한다. 
SBERT, KoSimCSE와 같은 사전학습된 모델을 이용하여 문장의 의미를 벡터로 변환한 뒤,  
평균(MEAN) 또는 Self-Attention 방식으로 문장 벡터를 통합한다. 

---

## 📂 파일 구성

| 파일명 | 설명 |
|--------|------|
| `sbert_embedding.py` | SBERT(Sentence-BERT)를 활용한 임베딩 클래스 |
| `kosimcse_embedding.py` | KoSimCSE 모델을 이용한 문장 임베딩 |
| `embedding_pooling.py` | 문장 임베딩 벡터에 대한 Mean / Self-Attention 풀링 기법 |

---

## 📘 클래스 설명

### 🔹 `SBERTModel`

```python
from embeddings.sbert_embedding import SBERTModel
model = SBERTModel()
embeddings = model.encode(sentences, return_all=True)