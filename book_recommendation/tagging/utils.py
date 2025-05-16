from typing import List, Dict, Any

def filtered_books_by_category(books: List[Dict[str, Any]], categories: List[str], category_level: int = 1) -> List[Dict[str, Any]]:
    """카테고리별로 도서를 필터링합니다."""
    filtered_books = []
    for book in books:
        if not book.get("category"):
            continue
            
        book_categories = book["category"]
        if isinstance(book_categories, str):
            book_categories = [book_categories]
            
        for category in categories:
            if any(category in cat.split("/")[category_level-1] for cat in book_categories):
                filtered_books.append(book)
                break
                
    return filtered_books


def exclude_books_by_category(books: List[Dict[str, Any]], categories: List[str]) -> List[Dict[str, Any]]:
    """특정 카테고리를 제외한 도서를 필터링합니다."""
    filtered_books = []
    for book in books:
        if not book.get("category"):
            continue
            
        book_categories = book["category"]
        if isinstance(book_categories, str):
            book_categories = [book_categories]
            
        if not any(category in cat for cat in book_categories for category in categories):
            filtered_books.append(book)
                
    return filtered_books


def filtered_books_by_page(books: List[Dict[str, Any]], max_pages: int) -> List[Dict[str, Any]]:
    """페이지 수로 도서를 필터링합니다."""
    return [book for book in books if book.get("page", 0) <= max_pages]
