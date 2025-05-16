import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List


class GenreClassifier:
    def __init__(self):
        # SBERT 모델 로드
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        
        # 장르 정의
        self.genres = {
            'literature': {
                'name': '문학',
                'keywords': ['소설', '시', '수필', '시집', '시인', '작가', '문학', '문장', '글쓰기']
            },
            'non_literature': {
                'name': '비문학',
                'keywords': ['경제', '경영', '과학', '역사', '철학', '심리', '자기계발', '건강', '취미']
            }
        }
        
        # 장르 키워드 임베딩 미리 계산
        self.genre_embeddings = {}
        for genre, info in self.genres.items():
            self.genre_embeddings[genre] = self.model.encode(info['keywords'])
    
    def classify_genre(self, text: str) -> Dict:
        """
        텍스트의 장르를 분류합니다.
        """
        try:
            # 텍스트 임베딩
            text_embedding = self.model.encode(text)
            
            # 각 장르별 유사도 계산
            genre_scores = {}
            for genre, embeddings in self.genre_embeddings.items():
                # 각 키워드와의 유사도 계산
                similarities = np.dot(embeddings, text_embedding) / (
                    np.linalg.norm(embeddings, axis=1) * np.linalg.norm(text_embedding)
                )
                # 평균 유사도 계산
                genre_scores[genre] = float(np.mean(similarities))
            
            # 가장 높은 점수의 장르 선택
            best_genre = max(genre_scores.items(), key=lambda x: x[1])
            
            return {
                'genre': self.genres[best_genre[0]]['name'],
                'score': best_genre[1],
                'all_scores': {
                    self.genres[genre]['name']: score
                    for genre, score in genre_scores.items()
                }
            }
        except Exception as e:
            st.error(f"장르 분류 중 오류가 발생했습니다: {str(e)}")
            return None


def display_genre_classification(result: Dict):
    """
    장르 분류 결과를 Streamlit에 표시합니다.
    """
    if not result:
        st.warning("장르를 분류할 수 없습니다.")
        return
        
    st.subheader("장르 분류 결과")
    
    # 예측된 장르 표시
    st.write(f"**예측된 장르**: {result['genre']}")
    
    # 각 장르별 점수 표시
    st.write("**장르별 점수**:")
    for genre, score in result['all_scores'].items():
        score_percent = int(score * 100)
        st.write(f"{genre}")
        st.progress(score_percent / 100)
        st.write(f"유사도: {score_percent}%")
        st.write("---") 