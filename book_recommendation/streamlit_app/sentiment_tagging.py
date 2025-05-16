import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import torch


class SentimentTagger:
    def __init__(self):
        # SBERT 모델 로드
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        
        # 감성 태그 정의
        self.sentiment_tags = [
            "유쾌한", "잔잔한", "흥미진진한", "서늘한",
            "따뜻한", "감동적인", "신비로운", "우울한",
            "활기찬", "평화로운"
        ]
        
        # 태그 임베딩 미리 계산
        self.tag_embeddings = self.model.encode(self.sentiment_tags)
    
    def get_sentiment_tags(self, text: str, top_k: int = 3) -> List[Dict]:
        """
        텍스트에 대한 감성 태그를 추천합니다.
        """
        # 텍스트 임베딩
        text_embedding = self.model.encode(text)
        
        # 코사인 유사도 계산
        similarities = np.dot(self.tag_embeddings, text_embedding) / (
            np.linalg.norm(self.tag_embeddings, axis=1) * np.linalg.norm(text_embedding)
        )
        
        # 상위 k개 태그 선택
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'tag': self.sentiment_tags[idx],
                'score': float(similarities[idx])
            })
            
        return results


def display_sentiment_tags(tags: List[Dict]):
    """
    감성 태그 결과를 Streamlit에 표시합니다.
    """
    if not tags:
        st.warning("태그를 추출할 수 없습니다.")
        return
        
    st.subheader("추천 감성 태그")
    
    # 태그를 점수 순으로 정렬하여 표시
    for tag in tags:
        score = tag['score']
        # 점수를 0-100 사이로 변환
        score_percent = int(score * 100)
        
        # 프로그레스 바로 점수 표시
        st.write(f"**{tag['tag']}**")
        st.progress(score_percent / 100)
        st.write(f"유사도: {score_percent}%")
        st.write("---") 