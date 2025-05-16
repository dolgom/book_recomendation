from keyword_extraction.keyword_extractor import TFIDFExtractor, TextRankExtractor
from json_utils import load_json, save_json
from tqdm import tqdm


def get_extractor(method='tfidf'):
    """키워드 추출 방법 선택"""
    if method == 'tfidf':
        return TFIDFExtractor()
    else:
        return TextRankExtractor()


def main(method='tfidf'):
    """키워드 추출"""
    extractor = get_extractor(method)
    # 📌 데이터 수정 필요: 저자까지 불용어처리한 데이터 넣어야 함!
    books = load_json("data/tagged_books.json")

    # 책 설명에서 키워드 추출
    for book in tqdm(books, desc="진행중", unit='book'):
        description = book.get("description", "")
        tags = extractor.extract_keywords(description)
        book["tags"] = tags
    save_json("data/word.json", books)
    print('완료!')
