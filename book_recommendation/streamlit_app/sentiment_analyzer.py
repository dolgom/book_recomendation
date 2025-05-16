from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np

# 감성 태그 정의
MOOD_TAGS = {
    "literature": [
        "감동적인", "따뜻한", "슬픈", "기쁜", "긴장감 있는", "로맨틱한",
        "신비로운", "유머러스한", "잔잔한", "지적인", "치유적인"
    ],
    "non_literature": [
        "실용적인", "전문적인", "흥미로운", "도전적인", "영감을 주는",
        "통찰력 있는", "혁신적인", "체계적인", "실험적인", "비판적인"
    ]
}

def get_mood_tags(text: str, category: str) -> List[str]:
    """
    텍스트의 감성을 분석하여 적절한 감성 태그를 반환합니다.
    
    Args:
        text (str): 분석할 텍스트
        category (str): 도서 카테고리 ("literature" 또는 "non_literature")
        
    Returns:
        List[str]: 매칭된 감성 태그 리스트
    """
    model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
    
    # 텍스트 임베딩
    text_embedding = model.encode(text)
    
    # 감성 태그 임베딩
    mood_embeddings = model.encode(MOOD_TAGS[category])
    
    # 코사인 유사도 계산
    similarities = np.dot(mood_embeddings, text_embedding) / (
        np.linalg.norm(mood_embeddings, axis=1) * np.linalg.norm(text_embedding)
    )
    
    # 상위 3개 감성 태그 선택
    top_indices = np.argsort(similarities)[-3:]
    selected_tags = [MOOD_TAGS[category][i] for i in top_indices]
    
    return selected_tags 