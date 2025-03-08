# 📚 yes24에서 큰글자도서의 정보를 스크래핑하기

## 프로젝트 구조
~~~
yes24_scraper/         
├── data/              # 스크래핑 결과(JSON 파일)가 저장될 폴더
├── scripts/           # 스크래핑 관련 스크립트 폴더
│   ├── scraper.py     # 스크래퍼(main)
│   ├── utils.py       # 스크래핑 관련 유틸리티 함수들
│   └── merge_json.py  # 여러 JSON 파일을 합치기
├── README.md          
└── requirements.txt   # 필요한 파이썬 패키지 목록
~~~

## 주요 기능
: yes24에서 큰글자도서 정보(도서명, 저자, 카테고리, 페이지 수, 책 소개) 크롤링해 JSON 파일로 저장

## 설치 및 설정
### 1. 가상 환경 생성 및 활성화
~~~
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
~~~

### 2. 필요한 패키지 설치
~~~
pip install -r requirements.txt
~~~
✔️ requirements.txt에 포함된 패키지
- requests
- beautifulsoup4
- tqdm

## 실행 방법
프로젝트 루트(yes24_scraper/)에서 다음 명령어 실행
~~~
python scripts/scraper.py 시작 페이지 끝 페이지
~~~
