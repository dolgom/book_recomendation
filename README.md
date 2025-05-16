# 📚 큰 글자 도서 검색 및 추천 서비스

yes24를 통해 다양한 책의 메타데이터를 수집한다. 

책 소개글을 기반으로 책의 **감성 분위기 태그**(예: "유쾌한", "잔잔한")를 자동으로 추천하고 키워드를 추출해 키워드로 책의 내용을 직관적으로 확인할 수 있다. 

yes24를 통해 다양한 책의 메타데이터를 수집합니다. 

책 소개글을 기반으로 책의 **감성 분위기 태그**(예: "유쾌한", "잔잔한")를 자동으로 추천하고 키워드를 추출해 키워드로 책의 내용을 직관적으로 확인할 수 있습니다. 

SBERT / KoSimCSE 임베딩과 다양한 풀링 전략을 통해 책 설명의 의미를 벡터화하고,  
코사인 유사도를 통해 가장 적절한 감성 태그를 예측한다. 

---

## 📁 프로젝트 구조
```
📁book_recommendation/
├── data/                        # 책 데이터(JSON), 키워드 추출 결과 등
│   ├── stopwords.txt
│   ├── word.json
│   └── literature.json ...
│
├── embeddings/                 # 임베딩 모델(SBERT, KoSimCSE) 및 풀링 
│   ├── sbert_embedding.py
│   ├── kosimcse_embedding.py
│   └── embedding_pooling.py
│
├── keyword_extraction/         # 키워드 추출 (TF-IDF, TextRank, 명사 토큰화)
│   ├── keyword_extractor.py
│   ├── noun_tokenizer.py
│   ├── author_stopwords.py
│   └── utils.py
│
├── tagging/                    # 감성 태그 추천기 및 전처리 유틸
│   ├── tag_recommender.py
│   └── utils.py
│
├── preprocessing/              # 문학/비문학 장르 분류 및 분량 필터링
│   └── genre_splitter.py
│
├── scripts/                    # 실행용 스크립트
│   ├── tagging_run.py          # 평균 풀링 기반 태그 추천 실행
│   ├── self_attention_run.py   # Self-Attention 풀링 기반 실행
│   └── kosimcse_run.py         # KoSimCSE 모델 실행
│
├── json_utils.py               # JSON 입출력 유틸 함수
└── README.md                   
```

---

## 🧩 주요 기능

### ✅ 감성 태그 추천
- 책 소개(description)을 문장 단위로 나눈 후 벡터 임베딩
- 다양한 풀링(MEAN, Self-Attention)을 통해 대표 벡터 생성
- 사전 정의된 감성 태그들과 코사인 유사도 비교

> 예시 태그: `"흥미진진한"`, `"잔잔한"`, `"유쾌한"`, `"서늘한"`

---

### ✅ 키워드 추출
- TF-IDF 기반 중요 단어 추출
- TextRank 기반 키워드 추출
- 명사 토큰화(Kiwi) 및 불용어 처리 포함  
- 작가 이름 자동 불용어 등록

---

### ✅ 데이터 전처리
- 문학/비문학 자동 분리
- 장르(한국소설, 외국소설, 시 등)별 분류
- 페이지 수 기반 필터링

---

## ⚙️ 설치 및 설정

### 1. 가상 환경 생성 및 활성화
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
```

📍 오류 시 Python 인터프리터를 추천 항목으로 변경해주세요

---

### 2. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

✔️ 포함 패키지:
- `torch`
- `transformers`
- `sentence-transformers`
- `scikit-learn`
- `kiwipiepy`
- `tqdm`
- `beautifulsoup4` (선택)

---

## 🚀 실행 방법

### 평균 풀링 방식 (SBERT)
```bash
python scripts/tagging_run.py
```

### Self-Attention 방식 (SBERT)
```bash
python scripts/self_attention_run.py
```

### KoSimCSE 모델로 태그 추천
```bash
python scripts/kosimcse_run.py
```

---

## 📎 참고

- [KoSimCSE 모델(HuggingFace)](https://huggingface.co/BM-K/KoSimCSE-roberta)
- [SBERT 공식 문서](https://www.sbert.net/)
- [kiwipiepy 형태소 분석기](https://github.com/bab2min/kiwipiepy)
