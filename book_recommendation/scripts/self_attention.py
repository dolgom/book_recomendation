from embeddings.sbert_embedding import SBERTModel
from embeddings.embedding_pooling import EmbeddingPooling
from tagging.tag_recommender import TagRecommender
from json_utils import load_json, save_json
from tqdm import tqdm

# 경로 설정
DATA_PATH = "data/literature.json"
OUTPUT_PATH = "data/attention_tagged_books.json"

# 태그 리스트 정의
recommendation_tags = ["흥미진진한", "잔잔한", "유쾌한", "서늘한"]

# SBERT 모델
embedding_model = SBERTModel()
pooling = EmbeddingPooling(embedding_model.attention_layer)
# 태그 추천 모델
tag_recommender = TagRecommender(model=embedding_model, tags=recommendation_tags, pooling=pooling)

books = load_json(DATA_PATH)
for book in tqdm(books, desc='진행중', unit='book'):
    description = book.get("description", "").strip()
    book["tag"] = tag_recommender.attention_recommend_tag(description)

save_json(books, OUTPUT_PATH)
print('종료!')
