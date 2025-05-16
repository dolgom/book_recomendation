import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from kiwipiepy import Kiwi
from typing import List, Dict
import numpy as np


class KeywordExtractor:
    def __init__(self):
        self.kiwi = Kiwi()
        self.tfidf = TfidfVectorizer(
            max_features=100,
            tokenizer=self._tokenize,
            stop_words=self._get_stopwords()
        )
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Kiwi를 사용하여 명사 토큰화를 수행합니다.
        """
        result = self.kiwi.analyze(text)
        nouns = []
        for token, pos, _ in result[0][0]:
            if pos.startswith('NN'):  # 명사만 추출
                nouns.append(token)
        return nouns
    
    def _get_stopwords(self) -> List[str]:
        """
        불용어 목록을 반환합니다.
        """
        return [
            '것', '이', '그', '저', '수', '등', '및', '또', '또는',
            '그리고', '하지만', '그러나', '그래서', '때문', '위해'
        ]
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[Dict]:
        """
        TF-IDF를 사용하여 키워드를 추출합니다.
        """
        try:
            # TF-IDF 계산
            tfidf_matrix = self.tfidf.fit_transform([text])
            feature_names = self.tfidf.get_feature_names_out()
            
            # 상위 k개 키워드 선택
            scores = tfidf_matrix.toarray()[0]
            top_indices = np.argsort(scores)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                results.append({
                    'keyword': feature_names[idx],
                    'score': float(scores[idx])
                })
                
            return results
        except Exception as e:
            st.error(f"키워드 추출 중 오류가 발생했습니다: {str(e)}")
            return []


def display_keywords(keywords: List[Dict]):
    """
    키워드 추출 결과를 Streamlit에 표시합니다.
    """
    if not keywords:
        st.warning("키워드를 추출할 수 없습니다.")
        return
        
    st.subheader("추출된 키워드")
    
    # 키워드를 점수 순으로 정렬하여 표시
    for keyword in keywords:
        score = keyword['score']
        # 점수를 0-100 사이로 변환
        score_percent = int(score * 100)
        
        # 프로그레스 바로 점수 표시
        st.write(f"**{keyword['keyword']}**")
        st.progress(score_percent / 100)
        st.write(f"중요도: {score_percent}%")
        st.write("---") 