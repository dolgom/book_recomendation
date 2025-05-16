import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from keyword_extraction.noun_tokenizer import NounTokenizer


class TFIDFExtractor:
    def __init__(self, top_n=5):
        self.vectorizer = TfidfVectorizer()
        self.top_n = top_n
        self.extractor = NounTokenizer()

    def extract_keywords(self, text):
        """TF-IDF 기반 키워드 추출"""
        noun_text = self.extractor.tokenize_nouns(text)  # 전처리 & 명사 추출
        tfidf_matrix = self.vectorizer.fit_transform([noun_text])  # TF-IDF 벡터화

        feature_names = np.array(self.vectorizer.get_feature_names_out())  # 단어 목록
        tfidf_scores = tfidf_matrix.toarray()[0]

        """상위 N개 키워드 선택"""
        top_indices = np.argsort(tfidf_scores)[::-1][:self.top_n]
        return feature_names[top_indices].tolist()


class TextRankExtractor:
    """TextRank 기반 키워드 추출"""
