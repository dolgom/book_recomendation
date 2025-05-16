# 🏷️ Tagging Module

이 모듈은 도서의 설명(description)을 바탕으로 감성 태그(예: "유쾌한", "잔잔한")를 추천하거나,  
도서 메타데이터(category, page 수 등)를 기준으로 도서를 필터링하는 유틸리티 함수들을 포함한다. 

---

## 📂 파일 구성
- `tag_recommender.py`  
  : 책 설명을 임베딩하고 코사인 유사도로 태그를 추천하는 클래스 (`TagRecommender`)
- `utils.py` 또는 `tag_recommender.py` 안에 포함된 함수들  
  : 카테고리 / 페이지 수를 기준으로 책을 필터링하는 유틸리티 함수들.

---

## 주요 클래스 및 함수 설명

### `TagRecommender`

책 설명과 사전 정의된 태그 사이의 유사도를 계산하여, 가장 적절한 태그를 추천한다. 

#### 초기화

```python
TagRecommender(model, tags, pooling, cache_dir='cache')
