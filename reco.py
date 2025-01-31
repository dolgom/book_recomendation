import streamlit as st
import google.generativeai as genai
import json
import re

# 키 설정
genai.configure(api_key='AIzaSyCbXoQ0d210OC4jLntlwFBAG9nKoa__vWg')
model = genai.GenerativeModel('gemini-1.5-flash')

# JSON 파일에서 도서 데이터 불러오기
with open('input.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

def get_book_recommendation(user_input):
    prompt = f"""
    다음은 책 제목과 책 소개 목록입니다:
    {json.dumps(books, ensure_ascii=False)}
    
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
        if book['검색어'].lower() in search_term.lower() or search_term.lower() in book['제목'].lower():
            return book['책표지']
    return None

st.title("도서 추천 챗봇")

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
