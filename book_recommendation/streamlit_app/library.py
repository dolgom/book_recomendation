import requests
import urllib.parse
from geopy.distance import geodesic
from bs4 import BeautifulSoup
import time
import re
import json

GOOGLE_MAPS_API_KEY = "AIzaSyAJ48wK0JK1wEmDrfwzQ_H94KPs64zIjn0"

def get_lat_lng(address, api_key):
    encoded_address = urllib.parse.quote_plus(address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        return None, None

libraries = [
    {"name": "송파도서관", "lat": 37.5072, "lng": 127.1269, "base_url": "https://splib.sen.go.kr", 
     "search_url": "https://splib.sen.go.kr/splib/intro/search/index.do?menu_idx=4&search_text={query}", 
     "call_number_keyword": "큰글"},
    # ... (중략: 도서관 목록 동일하게 추가)
]

def scrape_library(book_title, library_name, base_url, search_url, call_number_keyword):
    url = search_url.format(query=book_title)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[{library_name}] 요청 실패: {e}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("div", class_="bookStateBar")
    book_data = []
    for book in books:
        try:
            img_container = book.find_previous('div', class_='thumb')
            if img_container:
                img_tag = img_container.find('img')
                img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
                if not img_url.startswith('http'):
                    img_url = base_url + img_url
            else:
                img_url = 'https://splib.sen.go.kr/resources/common/img/noImg.gif'
            title_element = book.find_previous("a", class_="name goDetail")
            title = title_element.text.strip() if title_element else "제목 없음"
            author_element = book.find_previous("dd", class_="author").find("span")
            author = author_element.text.strip() if author_element else "저자 없음"
            call_number_element = book.find_previous("dd", class_="data").find("span", string=lambda text: text and "청구기호" in text)
            call_number = call_number_element.text.split(": ")[-1].strip() if call_number_element else "청구기호 없음"
            borrow_status_element = book.find("p", class_="txt")
            if borrow_status_element:
                borrow_status = borrow_status_element.get_text(strip=True)
                borrow_status = re.sub(r'<.*?>', '', borrow_status)
                borrow_status_ = "대출 가능" if "대출가능" in borrow_status else "대출 불가"
            else:
                borrow_status_ = "정보 없음"
            if call_number_keyword in call_number:
                book_data.append({
                    "도서관": library_name,
                    "제목": title,
                    "저자": author,
                    "청구 기호": call_number,
                    "대출 상태": borrow_status_,
                    "이미지": img_url
                })
        except Exception as e:
            print(f"[{library_name}] 내부 파싱 오류: {e}")
            continue
    return book_data

def get_books_from_all_libraries(book_title):
    all_books = []
    seen_books = set()
    for library in libraries:
        books = scrape_library(book_title, library["name"], library["base_url"], library["search_url"], library["call_number_keyword"])
        for book in books:
            book_key = (book["도서관"], book["제목"])
            if book_key not in seen_books:
                seen_books.add(book_key)
                all_books.append(book)
        time.sleep(2)
    return all_books

def run_full_library_search(book_title, user_address):
    books = get_books_from_all_libraries(book_title)
    if not books:
        return None, None
    default_img_url = "https://splib.sen.go.kr/resources/common/img/noImg.gif"
    selected_book = next((b for b in books if b["이미지"] != default_img_url), books[0])
    lat, lng = get_lat_lng(user_address, GOOGLE_MAPS_API_KEY)
    if not lat or not lng:
        return None, None
    distances = []
    for lib in libraries:
        dist = geodesic((lat, lng), (lib["lat"], lib["lng"])).km
        distances.append({"name": lib["name"], "distance": dist, "url": lib["base_url"], "lat": lib["lat"], "lng": lib["lng"]})
    distances.sort(key=lambda x: x["distance"])
    closest = distances[:3]
    lib_result = []
    for lib in closest:
        for book in books:
            if book["도서관"] == lib["name"]:
                lib_result.append({
                    "도서관": lib["name"],
                    "거리": lib["distance"],
                    "대출 상태": book["대출 상태"],
                    "url": lib["url"]
                })
    libraries_json = json.dumps(closest, ensure_ascii=False)
    map_html = f"""
    <!DOCTYPE html>
    <html lang=\"ko\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <script src=\"https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap\" async defer></script>
        <script>
            function initMap() {{
                var center = {{ lat: {lat}, lng: {lng} }};
                var map = new google.maps.Map(document.getElementById('map'), {{
                    zoom: 12,
                    center: center,
                    zoomControl: true,
                    gestureHandling: "auto"
                }});
                new google.maps.Marker({{
                    position: center,
                    map: map,
                    title: "사용자 위치",
                    icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                }});
                var libraries = {libraries_json};
                libraries.forEach(lib => {{
                    var marker = new google.maps.Marker({{
                        position: {{ lat: lib.lat, lng: lib.lng }},
                        map: map,
                        title: lib.name,
                        icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
                    }});
                }});
            }}
        </script>
    </head>
    <body>
        <div id=\"map\" style=\"width: 100%; height: 500px;\"></div>
    </body>
    </html>
    """
    book_info = {
        "제목": selected_book["제목"],
        "저자": selected_book["저자"],
        "이미지": selected_book["이미지"],
        "도서관들": lib_result
    }
    return book_info, map_html 