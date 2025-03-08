import requests
import html
from bs4 import BeautifulSoup

BASE_URL = 'http://yes24.com'


# 큰글자도서 검색 페이지에서 책 제목과 상세페이지 URL 가져오기
def get_url_from_page(soup):
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


# 상세 페이지에서 제목 추출
def get_title(soup):
    title = soup.find('h2', class_='gd_name')
    if title:
        return title.text.strip()
    else:
        return '제목 없음'


# 상세 페이지에서 저자 추출
def get_author(soup, title):
    author = soup.find('span', class_='gd_auth')
    if author:
        return author.find('a').text.strip()
    else:
        print(f'{title}, 저자')
        return '저자 정보 없음'


# 책 소개 추출
def get_description(soup, title):
    text_area = soup.find('textarea', class_='txtContentText')
    if text_area:
        description = text_area.get_text().strip()
        return html.unescape(description)  # HTML 엔티티를 원래 텍스트로 변환
    else:
        print(f'{title}, 책소개')
        return '책소개 정보 없음'


# 쪽수 추출
def get_pages(soup, title):
    size = soup.find('th', class_='txt', string=lambda x: x and '쪽수, 무게, 크기' in x)
    if size:
        return size.find_next('td', class_='txt lastCol').text.split(' | ')[0].strip()
    else:
        print(f'{title}, 쪽수')
        return '쪽수 정보 없음'


# 카테고리 추출
def get_category(soup, title):
    category_section = soup.find('dl', class_='yesAlertDl').find_all('a')

    for i, section in enumerate(category_section):
        if section.text.strip() == '국내도서':
            if i + 1 < len(category_section):
                return category_section[i + 1].text.strip()
            else:
                print(f'{title}, 카테고리')
                return '국내도서'


# 상세페이지에서 전체 정보 가져오기
def get_book_info(book_url):
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
