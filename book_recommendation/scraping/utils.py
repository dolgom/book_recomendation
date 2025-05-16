import requests
import html
from bs4 import BeautifulSoup
import re

BASE_URL = 'http://yes24.com'


def get_url_from_page(soup):
    """큰글자도서 검색 페이지에서 책 제목과 상세페이지 URL 가져오기"""
    book_urls = []
    book_list = soup.find_all('div', class_='info_row info_name')

    for book in book_list:
        # 제목 추출
        title_tag = book.find('a', class_='gd_name')
        # 상세페이지 URL 추출
        if title_tag and 'Category/Series' not in title_tag.get('href', ''):
            book_url = BASE_URL + title_tag.get('href')
            book_urls.append(book_url)

    return book_urls


def get_title(soup):
    """상세 페이지에서 제목 추출"""
    title = soup.find('h2', class_='gd_name')
    if title:
        title = title.text.strip()
        title_clean = re.sub(r'\s*[\(\[].*?[\)\]]', '', title)
        title_clean = re.sub(r'\s*큰글\S*', '', title_clean)
        return title_clean
    else:
        return '제목 없음'


def get_author(soup, title):
    """상세 페이지에서 저자 추출"""
    author = soup.find('span', class_='gd_auth')
    if author:
        a_tag = author.find('a')
        if a_tag:
            return a_tag.text.strip()
        else:
            print(f'[저자] {title}')
            return '저자 정보 없음'
    else:
        print(f'[저자] {title}')
        return '저자 정보 없음'


def get_description(soup, title):
    """책 소개 추출"""
    text_area = soup.find('textarea', class_='txtContentText')
    if text_area:
        description = text_area.get_text().strip()
        return html.unescape(description)  # HTML 엔티티를 원래 텍스트로 변환
    else:
        print(f'[책소개] {title}')
        return '책소개 정보 없음'


def get_pages(soup, title):
    """쪽수 추출"""
    size = soup.find('th', class_='txt', string=lambda x: x and '쪽수, 무게, 크기' in x)
    if size:
        return size.find_next('td', class_='txt lastCol').text.split(' | ')[0].strip()
    else:
        print(f'[쪽수] {title}')
        return '쪽수 정보 없음'


def get_category(soup, title):
    """카테고리 추출"""
    category_section = soup.find('dl', class_='yesAlertDl').find_all('a')

    if not category_section:
        print(f'[카테고리] {title}')
        return '카테고리 정보 없음'

    categories = []
    for section in category_section:
        text = section.text.strip()
        if text != '국내도서':
            categories.append(text)

    category_dict = {}
    index = 1
    for cate in categories:
        category_dict[f'category{index}'] = cate
        index += 1

    return category_dict


def get_book_info(book_url):
    """상세페이지에서 전체 정보 가져오기"""
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = get_title(soup)

    return {
        'title': title,
        'author': get_author(soup, title),
        'description': get_description(soup, title),
        'pages': get_pages(soup, title),
        'category': get_category(soup, title)
    }
