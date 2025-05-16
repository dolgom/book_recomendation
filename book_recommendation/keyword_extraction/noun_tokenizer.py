import re
from kiwipiepy import Kiwi
from keyword_extraction.utils import load_stopwords


class NounTokenizer:
    """형태소 분석"""
    def __init__(self):
        self.kiwi = Kiwi()
        self.stopwords = load_stopwords()

    def clean_text(self, text):
        """한글, 숫자, 공백만 남기고 특수문자 제거"""
        return re.sub(r'[^가-힣0-9\s]', '', text)

    def tokenize_nouns(self, text):
        """형태소 분석을 통해 명사(N)만 추출"""
        text = self.clean_text(text)
        words = self.kiwi.tokenize(text)
        nouns = [word.form for word in words if word.tag.startswith("N") and word.form not in self.stopwords]
        return nouns
