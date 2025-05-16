import requests
from bs4 import BeautifulSoup
import time


def scrape_library(book_title, library):
    url = library["search_url"].format(query=book_title)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("div", class_="bookStateBar")

    result = []
    for book in books:
        try:
            img_tag = book.find_previous("div", class_="thumb")
            img_url = "https://splib.sen.go.kr/resources/common/img/noImg.gif"
            if img_tag:
                img = img_tag.find("img")
                if img and "src" in img.attrs:
                    src = img["src"]
                    img_url = src if src.startswith("http") else library["base_url"] + src

            title = book.find_previous("a", class_="name goDetail")
            author = book.find_previous("dd", class_="author").find("span")
            call_no_elem = book.find_previous("dd", class_="data").find("span", string=lambda t: "청구기호" in t if t else False)
            call_number = call_no_elem.text.split(": ")[-1].strip() if call_no_elem else "청구기호 없음"

            borrow_elem = book.find("p", class_="txt")
            borrow_text = borrow_elem.get_text(strip=True) if borrow_elem else "정보 없음"
            status = "대출 가능" if "대출가능" in borrow_text else "대출 불가"

            if library["call_number_keyword"] in call_number:
                result.append({
                    "도서관": library["name"],
                    "제목": title.text.strip() if title else "제목 없음",
                    "저자": author.text.strip() if author else "저자 없음",
                    "청구 기호": call_number,
                    "대출 상태": status,
                    "이미지": img_url
                })
        except Exception:
            continue
    return result


def get_books_from_all_libraries(book_title, libraries):
    all_books = []
    seen = set()
    for lib in libraries:
        books = scrape_library(book_title, lib)
        for book in books:
            key = (book["도서관"], book["제목"])
            if key not in seen:
                seen.add(key)
                all_books.append(book)
        time.sleep(2)
    return all_books
