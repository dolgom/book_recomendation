import streamlit as st
import sys
import os
import json
import requests
import urllib.parse
from geopy.distance import geodesic
from bs4 import BeautifulSoup
import time
import re

# 상위 디렉토리를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 모듈 임포트
from streamlit_app.book_search import check_borrow_possible, display_search_results
from streamlit_app.sentiment_tagging import SentimentTagger, display_sentiment_tags
from streamlit_app.keyword_extraction import KeywordExtractor, display_keywords
from streamlit_app.genre_classifier import GenreClassifier, display_genre_classification
from streamlit_app.recommendation import get_recommendations
from library import get_books_from_all_libraries, get_lat_lng, libraries, run_full_library_search

def display_book(book):
    st.markdown(f"### {book['title']}")
    st.write(f"**저자:** {book['author']}")
    st.write(f"**키워드:** {', '.join(book.get('keywords', []))}")
    st.write(f"**분위기:** {book.get('mood_tags', [''])[0]}")

def get_unique_categories(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        books = json.load(f)
    categories = set()
    for book in books:
        cat = book.get('category')
        if isinstance(cat, list):
            categories.update(cat)
        elif isinstance(cat, str):
            categories.add(cat)
    return sorted(list(categories))

# 도서관별 도서 정보 출력 함수 (반드시 페이지 분기문보다 위에 위치)
def display_library_books(books):
    if not books:
        st.info("검색 결과가 없습니다.")
        return
    for book in books:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(book["이미지"], width=120)
            with cols[1]:
                st.markdown(f"**{book['제목']}**")
                st.write(f"저자: {book['저자']}")
                st.write(f"도서관: {book['도서관']}")
                st.write(f"청구 기호: {book['청구 기호']}")
                st.write(f"대출 상태: {book['대출 상태']}")
        st.markdown("---")

# 페이지 설정
st.set_page_config(
    page_title="도서 추천 시스템",
    page_icon="📚",
    layout="wide"
)

# 사이드바
st.sidebar.title("📚큰글자도서 검색 및 추천")
page = st.sidebar.selectbox(
    "기능 선택",
    ["홈", "이달의 도서", "도서 검색", "도서 추천", "도서관 찾기"]
)

# 모델 초기화
@st.cache_resource
def _load_models():
    """모델 로딩 함수"""
    with st.spinner('모델을 로딩하는 중입니다...'):
        return {
            'sentiment_tagger': SentimentTagger(),
            'keyword_extractor': KeywordExtractor(),
            'genre_classifier': GenreClassifier()
        }

# 모델 로딩
models = _load_models()

# 홈 페이지
if page == "홈":
    st.markdown("""
        <style>
        .home-center {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding-top: 0;
            margin-top: 0;
        }
        .home-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #111;
            margin-bottom: 1.5em;
            text-align: center;
        }
        .home-desc {
            font-size: 1.15rem;
            color: #333;
            margin-bottom: 2em;
            text-align: center;
        }
        .home-highlight {
            font-size: 1.7rem;
            font-weight: bold;
            color: #1a3c7b;
            margin-top: 1.5em;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="home-center">', unsafe_allow_html=True)
    st.markdown('<div class="home-title">🔎큰글자도서 검색 및 추천 서비스</div>', unsafe_allow_html=True)
    st.markdown('<div class="home-desc">작은 글씨 때문에 책 읽기 불편하셨나요?<br>이제, 큰글자도서를 쉽고 빠르게 찾아보세요!<br><br>취향에 맞는 큰글자책 추천<br>원하는 책을 쉽게 검색<br>소장 도서와 대출 가능 여부 확인<br>지도에서 가까운 도서관 위치까지 한눈에!</div>', unsafe_allow_html=True)
    st.markdown(
        '''
        <div style="display: flex; justify-content: center;">
            <img src="https://i.namu.wiki/i/prkqXmURVT6m5TC4YROJ_x0Dlp7jWYhMNxWAR2j8QGAl0m8C5nalADbLz3-uWMidObbdDAM9jRueVQFLWK_9d_isiwX063v0UZ_9VWEcWaospzlXaaVtv2Fnnr1LV1f2CVnPqTNgV3FzArFQdbuWJg.webp" width="420">
        </div>
        ''',
        unsafe_allow_html=True
    )
    st.markdown('<div class="home-highlight">지금, 더 편리한 독서를 시작해보세요.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 도서 검색 페이지
elif page == "도서 검색":
    st.title('📚송파도서관 큰글자 도서 검색')

    # 세션 상태 초기화
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False

    user_input = st.text_input("검색할 도서 제목을 입력하세요:", key="search_input")

    if user_input:
        search_results = check_borrow_possible(user_input)
        display_search_results(search_results)
        st.session_state.search_performed = True
    elif st.session_state.search_performed:
        st.session_state.search_performed = False
        st.experimental_rerun()

# 감성 태그 추천 페이지
elif page == "감성 태그 추천":
    st.title("🏷️ 감성 태그 추천")
    book_description = st.text_area("도서 설명을 입력하세요")
    if st.button("태그 추천"):
        if book_description:
            with st.spinner("태그를 추천하는 중..."):
                tags = models['sentiment_tagger'].get_sentiment_tags(book_description)
                display_sentiment_tags(tags)

# 키워드 추출 페이지
elif page == "키워드 추출":
    st.title("🔑 키워드 추출")
    text = st.text_area("텍스트를 입력하세요")
    if st.button("키워드 추출"):
        if text:
            with st.spinner("키워드를 추출하는 중..."):
                keywords = models['keyword_extractor'].extract_keywords(text)
                display_keywords(keywords)

# 장르 분류 페이지
elif page == "장르 분류":
    st.title("📖 장르 분류")
    book_info = st.text_area("도서 정보를 입력하세요")
    if st.button("분류"):
        if book_info:
            with st.spinner("장르를 분류하는 중..."):
                result = models['genre_classifier'].classify_genre(book_info)
                display_genre_classification(result)

# 도서 추천 페이지
elif page == "도서 추천":
    tab1, tab2 = st.tabs(["태그 기반 추천", "자유로운 추천 (Gemini)"])
    with tab1:
        # 분위기 태그 정의
        mood_tags = {
            "문학": ["지적인", "따뜻한", "감동적인", "서늘한", "상관없음"],
            "비문학": ["실용적인", "전문적인", "체계적인", "영감을 주는", "상관없음"]
        }
        category = st.selectbox("도서 분류", ["문학", "비문학"])
        if category == "문학":
            genre_options = [
                "한국소설", "외국소설", "시/희곡", "고전문학", "에세이", "상관없음"
            ]
        else:
            genre_options = [
                "인문", "사회 정치", "예술", "역사", "경제 경영", "자기계발", "건강 취미", "자연과학", "IT 모바일", "청소년", "가정살림", "만화/라이트노벨", "상관없음"
            ]
        genre = st.selectbox("세부 장르", genre_options)
        max_pages = st.slider("최대 페이지 수", 0, 1000, 500, step=100)
        selected_mood = st.selectbox("분위기 태그", mood_tags[category])
        if st.button("도서 추천받기", key="tag_recommend"):
            with st.spinner("도서를 추천하고 있습니다..."):
                recommendations = get_recommendations(category, genre, max_pages, selected_mood)
                if selected_mood != "상관없음":
                    recommendations = [book for book in recommendations if selected_mood in book.get("mood_tags", [])]
                if recommendations:
                    st.subheader("추천 도서")
                    for idx, book in enumerate(recommendations):
                        display_book(book)
                        if idx < len(recommendations) - 1:
                            st.markdown("---")
                else:
                    st.warning("조건에 맞는 도서를 찾을 수 없습니다.")
    with tab2:
        import google.generativeai as genai
        import re
        import json as pyjson
        api_key = "AIzaSyCoJFqlZ8BPqJlp40-1INO--1ADLwcva5g"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # 기존 도서 JSON 파일 사용
        with open('data/filtered_tag/books_test.json', 'r', encoding='utf-8') as f:
            books = pyjson.load(f)
        def get_book_recommendation(user_input):
            prompt = f"""
            다음은 책 제목과 책 소개 목록입니다:
            {pyjson.dumps(books, ensure_ascii=False)}
            
            사용자 입력: {user_input}
            
            위 도서 목록에서 사용자의 관심사에 맞는 책을 3권 추천하고, 각 책에 대한 자세한 설명을 제공해주세요.
            정렬은 판매지수가 높은 순서대로 부탁합니다. 판매지수 표시는 하지 말아주세요.
            각 추천은 다음 형식으로 제공해주세요:
            제목: [책의 검색어]

            설명: [책에 대한 자세한 설명 (최대 200자)]
            """
            response = model.generate_content(prompt)
            return response.text
        def extract_recommendations(text):
            recommendations = re.split(r'\n\n(?=제목:)', text)
            return [rec.strip() for rec in recommendations if rec.strip()]
        def find_book_cover(search_term):
            for book in books:
                if book['검색어'] in search_term or search_term in book['제목']:
                    return book['책표지']
            return None
        st.title("큰글자도서 자유 추천📕")
        user_input = st.text_input("어떤 책을 찾고 계신가요? (예시: 여행 관련 책 추천)")
        if user_input:
            recommendation_text = get_book_recommendation(user_input)
            recommendations = extract_recommendations(recommendation_text)
            for rec in recommendations:
                parts = rec.split('\n\n', 1)
                if len(parts) == 2:
                    title_part, description_part = parts
                    search_term_match = re.search(r'제목: (.+)', title_part)
                    if search_term_match:
                        search_term = search_term_match.group(1)
                        cover_url = find_book_cover(search_term)
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if cover_url:
                                st.image(cover_url, width=150)
                            else:
                                st.write("책 표지를 찾을 수 없습니다.")
                        with col2:
                            st.write(title_part)
                            st.write(description_part)
                else:
                    st.write(rec)

# 이달의 도서 페이지
elif page == "이달의 도서":
    st.markdown("""
        <style>
        .month-title {
            font-size: 3.2rem;
            font-weight: bold;
            color: #111;
            margin-bottom: 0.2em;
            text-align: center;
        }
        .main-img-center {
            width: 100%;
            margin-bottom: 1.2em;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="month-title">🌱5월 도서 추천</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-img-center" style="margin-bottom:1.2em;">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:center; margin-top:0;"><img src="https://ifh.cc/g/XmZLnY.jpg" width="750"></div>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:center; margin-top:1.2em;"><img src="https://ifh.cc/g/0odHN0.jpg" width="650"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 도서관 찾기 페이지 (지도/거리 기반만)
elif page == "도서관 찾기":
    st.header("📍 큰글자도서 보유 도서관 찾기")
    book = st.text_input("도서 제목 입력")
    address = st.text_input("주소 또는 역 이름 입력")
    if st.button("도서관 검색"):
        with st.spinner("도서관 정보를 검색 중입니다..."):
            books, map_html = run_full_library_search(book, address)
        if books:
            st.success("✅ 검색이 완료되었습니다!")
            st.image(books["이미지"], width=200)
            st.write(f"**제목:** {books['제목']}")
            st.write(f"**저자:** {books['저자']}")
            st.subheader("📍 가까운 도서관 목록")
            for lib in books["도서관들"]:
                status = "🟢 대출 가능" if "가능" in lib["대출 상태"] else "🔴 대출 불가"
                st.markdown(
                    f"- **{lib['도서관']}** (거리: {lib['거리']:.2f} km) - {status}  \n"
                    f"[도서관 홈페이지 이동]({lib['url']})"
                )
            st.components.v1.html(map_html, height=500)
        else:
            st.error("❌ 검색 결과를 찾을 수 없습니다.")

# --- 도서관 찾기용 함수 및 데이터 ---
libraries = [
    {"name": "송파도서관", "lat": 37.5072, "lng": 127.1269, "base_url": "https://splib.sen.go.kr", 
     "search_url": "https://splib.sen.go.kr/splib/intro/search/index.do?menu_idx=4&search_text={query}", 
     "call_number_keyword": "큰글"},
    # ... (중략: 도서관 목록 동일하게 추가)
]

def scrape_library(book_title, library_name, base_url, search_url, call_number_keyword):
    url = search_url.format(query=book_title)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("div", class_="bookStateBar")
    book_data = []
    for book in books:
        try:
            img_container = book.find_previous('div', class_='thumb')
            if img_container:
                img_tag = img_container.find('img')
                img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
                if not img_url.startswith('http'):
                    img_url = base_url + img_url
            else:
                img_url = 'https://splib.sen.go.kr/resources/common/img/noImg.gif'
            title_element = book.find_previous("a", class_="name goDetail")
            title = title_element.text.strip() if title_element else "제목 없음"
            author_element = book.find_previous("dd", class_="author").find("span")
            author = author_element.text.strip() if author_element else "저자 없음"
            call_number_element = book.find_previous("dd", class_="data").find("span", string=lambda text: text and "청구기호" in text)
            call_number = call_number_element.text.split(": ")[-1].strip() if call_number_element else "청구기호 없음"
            borrow_status_element = book.find("p", class_="txt")
            if borrow_status_element:
                borrow_status = borrow_status_element.get_text(strip=True)
                borrow_status = re.sub(r'<.*?>', '', borrow_status)
                borrow_status_ = "대출 가능" if "대출가능" in borrow_status else "대출 불가"
            else:
                borrow_status_ = "정보 없음"
            if call_number_keyword in call_number:
                book_data.append({
                    "도서관": library_name,
                    "제목": title,
                    "저자": author,
                    "청구 기호": call_number,
                    "대출 상태": borrow_status_,
                    "이미지": img_url
                })
        except Exception as e:
            continue
    return book_data

def get_books_from_all_libraries(book_title):
    all_books = []
    seen_books = set()
    for library in libraries:
        books = scrape_library(book_title, library["name"], library["base_url"], library["search_url"], library["call_number_keyword"])
        for book in books:
            book_key = (book["도서관"], book["제목"])
            if book_key not in seen_books:
                seen_books.add(book_key)
                all_books.append(book)
        time.sleep(2)
    return all_books 