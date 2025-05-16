from scraping.utils import get_url_from_page, get_book_info

import json
import requests
import sys
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data/raw_scraped') # 데이터 저장 경로

# URL 설정
SEARCH_URL = 'https://www.yes24.com/Product/Search?domain=BOOK&query=%25ED%2581%25B0%25EA%25B8%2580%25EC%259E%2590%25EB%258F%2584%25EC%2584%259C&page={}&statGbYn=Y&size=120'


def scrape_books(start_page, end_page):
    """페이지 스크래핑"""
    print('크롤링 시작')
    book_data = []

    for page_num in tqdm(range(start_page, end_page + 1)):
        url = SEARCH_URL.format(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        book_urls = get_url_from_page(soup)

        # book_info 리스트에 책 정보들 저장
        for book_url in book_urls:
            book_info = get_book_info(book_url)
            book_data.append(book_info)

        print(f'페이지: {page_num} 완료')

    # JSON 저장 폴더 확인 후 저장
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    filename = os.path.join(DATA_DIR, f'books_{start_page}_{end_page}.json')
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(book_data, json_file, ensure_ascii=False, indent=4)

    print(f"JSON 파일 저장 완료: {filename}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("코드 작성: python scraper.py 시작페이지 끝페이지")
        start_page = int(input('시작페이지 입력: '))
        end_page = int(input('끝페이지 입력: '))

    else:
        start_page = int(sys.argv[1])
        end_page = int(sys.argv[2])

    scrape_books(start_page, end_page)
