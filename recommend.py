import streamlit as st
import google.generativeai as genai
import json


# 키
genai.configure(api_key='AIzaSyCbXoQ0d210OC4jLntlwFBAG9nKoa__vWg')
model = genai.GenerativeModel('gemini-1.5-flash')

# JSON 파일에서 도서 데이터 불러오기
with open('books_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)


def get_book_recommendation(user_input):
    prompt = f"""
    다음은 책 제목과 책 소개 목록입니다:
    {json.dumps(books, ensure_ascii=False)}
    
    사용자 입력: {user_input}
    
    위 도서 목록에서 사용자의 관심사에 맞는 책을 3권 추천하고, 각 책에 대한 간단한 설명을 제공해주세요.
    """
    response = model.generate_content(prompt)
    return response.text

st.title("도서 추천 챗봇")

user_input = st.text_input("어떤 책을 찾고 계신가요? (예시: 여행 관련 책 추천)")

if user_input:
    recommendation = get_book_recommendation(user_input)
    st.write(recommendation)
