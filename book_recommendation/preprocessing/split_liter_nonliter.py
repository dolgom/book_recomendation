from tagging.utils import filtered_books_by_category, exclude_books_by_category
from json_utils import load_json, save_json

if __name__ == "__main__":
    """문학 비문학 나누기"""
    books = load_json("data/filtered_books_test.json") # 📌 데이터 변경 필요
    literature_books = filtered_books_by_category(books, ["소설/시/희곡", "에세이"])
    save_json(literature_books, "data/filtered_tag/literature.json")

    # 문학이 아닌 책들(non-literature) 저장
    non_literature_books = exclude_books_by_category(books, ["소설/시/희곡", "에세이"])
    save_json(non_literature_books, "data/filtered_tag/non_literature.json")

    print("완료")
