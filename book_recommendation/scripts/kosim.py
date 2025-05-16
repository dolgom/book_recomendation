from embeddings.kosimcse_embedding import KoSimCSEEmbedding
from embeddings.embedding_pooling import EmbeddingPooling
from tagging.tag_recommender import TagRecommender
from json_utils import load_json, save_json
from tqdm import tqdm
import streamlit as st

# 경로 설정
DATA_PATH = "data/literature.json"
OUTPUT_PATH = "data/kosim_tagged_books.json"

# 태그 리스트 정의
recommendation_tags = ["흥미진진한", "잔잔한", "유쾌한", "서늘한"]

# SBERT 모델
embedding_model = KoSimCSEEmbedding()
pooling = EmbeddingPooling(embedding_model.attention_layer)

tag_recommender = TagRecommender(model=embedding_model, tags=recommendation_tags, pooling=pooling)

books = load_json(DATA_PATH)
for book in tqdm(books, desc='진행중', unit='book'):
    description = book.get("description", "").strip()
    book["tag"] = tag_recommender.mean_recommend_tag(description)

save_json(books, OUTPUT_PATH)
print('종료!')

def display_library_books(books):
    if not books:
        st.info("검색 결과가 없습니다.")
        return
    for book in books:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(book["이미지"], width=120)
            with cols[1]:
                st.markdown(f"**{book['제목']}**")
                st.write(f"저자: {book['저자']}")
                st.write(f"도서관: {book['도서관']}")
                st.write(f"청구 기호: {book['청구 기호']}")
                st.write(f"대출 상태: {book['대출 상태']}")
        st.markdown("---")

# --- 그 아래에 페이지 분기문 ---
# if page == "도서관 찾기":
#     ...
#     display_library_books(books)
