import streamlit as st
import json
from pathlib import Path
from typing import List, Dict, Any
import random

def load_books(category: str) -> List[Dict[str, Any]]:
    """도서 데이터를 로드합니다."""
    data_path = Path("data/filtered_tag")
    # 카테고리 매핑
    category_mapping = {
        "문학": "literature",
        "비문학": "non_literature"
    }
    category = category_mapping.get(category, category)
    
    if category == "literature":
        with open(data_path / "literature.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(data_path / "non_literature.json", "r", encoding="utf-8") as f:
            return json.load(f)

def filter_by_genre(books: List[Dict[str, Any]], genre: str) -> List[Dict[str, Any]]:
    """장르별로 도서를 필터링합니다."""
    # 장르 매핑
    genre_mapping = {
        "소설": ["소설", "한국소설", "외국소설"],
        "시": ["시", "시/희곡"],
        "에세이": ["에세이", "인문에세이"],
        "인문": ["인문", "인문/심리", "인문/철학"],
        "자연과학": ["자연과학", "자연과학/뇌과학"],
        "건강취미": ["건강취미", "건강취미/건강정보"]
    }
    
    target_genres = genre_mapping.get(genre, [genre])
    return [book for book in books if any(g in "/".join(book.get("category", [])) for g in target_genres)]

def filter_by_volume(books: List[Dict[str, Any]], max_pages: int) -> List[Dict[str, Any]]:
    """페이지 수로 도서를 필터링합니다."""
    return [book for book in books if book.get("page", 0) <= max_pages]

def filter_by_mood(books: List[Dict[str, Any]], mood: str) -> List[Dict[str, Any]]:
    """분위기 태그로 도서를 필터링합니다."""
    return [book for book in books if mood in book.get("mood_tags", [])]

def get_recommendations(category: str, genre: str, max_pages: int, mood: str) -> List[Dict[str, Any]]:
    """도서 추천을 수행합니다."""
    books = load_books(category)
    
    # 장르 필터링
    if genre != "상관없음":
        books = filter_by_genre(books, genre)
    
    # 페이지 수 필터링
    if max_pages > 0:
        books = filter_by_volume(books, max_pages)
    
    # 분위기 태그 필터링
    if mood != "상관없음":
        books = filter_by_mood(books, mood)
    
    # 결과가 없으면 전체에서 무작위 추천
    if not books:
        books = load_books(category)
        random.shuffle(books)
        return books[:3]  # 3권 추천
    return books[:3]  # 3권 추천 