# 📚 Keyword Extraction for Book Descriptions

이 폴더는 책 소개글에서 **중요한 단어 기반 키워드**를 추출하기 위한 Python 모듈
TF-IDF, TextRank 알고리즘을 사용하며, 한국어 형태소 분석기 **Kiwi**를 기반으로 명사만을 추출하여 키워드들 추출한다. 

- TF-IDF 기반 키워드 추출
- TextRank 기반 키워드 추출
- 작가 이름 자동 불용어 처리
- Kiwi 한국어 형태소 분석기 이용해 명사 추출
- stopwords.txt 로 불용어 필터링