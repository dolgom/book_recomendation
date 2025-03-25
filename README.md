## 📁 프로젝트 구조 설명

- `📁 data/`  
  → 전처리된 데이터, JSON 파일, 불용어 목록 (`stopwords.txt`) 등을 저장

- `📁 embeddings/`  
  → SBERT, KoSimCSE 임베딩 및 풀링 전략 관련 모듈

- `📁 find_library/`  
  → 도서관 위치, 거리 계산, 대출 가능 여부 확인 등 위치 기반 기능

- `📁 keyword_extraction/`  
  → 명사 토크나이징, 작가 불용어 제거, 키워드 추출(TF-IDF, TextRank 등)

- `📁 preprocessing/`  
  → 문학/비문학 장르 분리 및 기타 전처리 로직

- `📁 tagging/`  
  → 책에 대한 감성 태그 자동 매칭 로직

- `📁 trending_searches/`  
  → 교보문고 실시간 검색어 크롤링 및 워드클라우드 생성 기능

- `📁 gemini_recommender/`  
  → Gemini API 기반 책 추천 로직

- `📁 scripts/`  
  → 위 기능들을 실행하기 위한 메인 진입점 스크립트들

- `📄 json_utils.py`  
  → JSON 파일 로드 및 저장 관련 모듈
