import requests
import urllib.parse
from geopy.distance import geodesic
from bs4 import BeautifulSoup
import time
import re
from PIL import Image
from io import BytesIO
import json

GOOGLE_MAPS_API_KEY = "AIzaSyAJ48wK0JK1wEmDrfwzQ_H94KPs64zIjn0"

#사용자가 입력한 주소로부터 위도, 경도를 불러옴
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

# 도서관 데이터 
libraries = [{"name": "송파도서관", "lat": 37.5072, "lng": 127.1269, "base_url": "https://splib.sen.go.kr", "search_url": "https://splib.sen.go.kr/splib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰글"},
             {"name": "강남도서관", "lat": 37.4979, "lng": 127.0276, "base_url": "https://gnlib.sen.go.kr", "search_url": "https://gnlib.sen.go.kr/gnlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "강동도서관", "lat": 37.5307, "lng": 127.1237, "base_url": "https://gdlib.sen.go.kr", "search_url": "https://gdlib.sen.go.kr/gdlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "특수"},
             {"name": "종로도서관", "lat": 37.5702, "lng": 126.9782, "base_url": "https://jnlib.sen.go.kr", "search_url": "https://jnlib.sen.go.kr/jnlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "남산도서관", "lat": 37.5547, "lng": 126.9750, "base_url": "https://nslib.sen.go.kr", "search_url": "https://nslib.sen.go.kr/nslib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "용산도서관", "lat": 37.5286, "lng": 126.9735, "base_url": "https://yslib.sen.go.kr", "search_url": "https://yslib.sen.go.kr/yslib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "특"},
             {"name": "동대문도서관", "lat": 37.5736, "lng": 127.0393, "base_url": "https://ddmlib.sen.go.kr", "search_url": "https://ddmlib.sen.go.kr/ddmlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰글"},
             {"name": "도봉도서관", "lat": 37.6583, "lng": 127.0280, "base_url": "https://dblib.sen.go.kr", "search_url": "https://dblib.sen.go.kr/dblib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "강서도서관", "lat": 37.5583, "lng": 126.8493, "base_url": "https://gslib.sen.go.kr", "search_url": "https://gslib.sen.go.kr/gslib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "서울시교육청 고덕평생학습관", "lat": 37.5541, "lng": 127.1224, "base_url": "https://gdllc.sen.go.kr", "search_url": "https://gdllc.sen.go.kr/gdllc/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰글"},
             {"name": "서울시교육청 고척도서관", "lat": 37.5155, "lng": 126.8482, "base_url": "https://gslib.sen.go.kr", "search_url": "https://gslib.sen.go.kr/gslib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "특"},
             {"name": "서울시교육청 구로도서관", "lat": 37.4993, "lng": 126.8842, "base_url": "https://grlib.sen.go.kr", "search_url": "https://grlib.sen.go.kr/grlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "서울시교육청 노원평생학습관", "lat": 37.6536, "lng": 127.0786, "base_url": "https://nwllc.sen.go.kr", "search_url": "https://nwllc.sen.go.kr/nwllc/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰글"},
             {"name": "서울시교육청 동작도서관", "lat": 37.5114, "lng": 126.9422, "base_url": "https://djlib.sen.go.kr", "search_url": "https://djlib.sen.go.kr/djlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "장"},
             {"name": "서울시교육청 마포평생아현분관", "lat": 37.5450, "lng": 126.9462, "base_url": "https://ahyon.sen.go.kr", "search_url": "https://ahyon.sen.go.kr/ahyon/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "서울시교육청 마포평생학습관", "lat": 37.5507, "lng": 126.9459, "base_url": "https://mpllc.sen.go.kr", "search_url": "https://mpllc.sen.go.kr/mpllc/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "서울시교육청 서대문도서관", "lat": 37.5613, "lng": 126.9674, "base_url": "https://sdmlib.sen.go.kr", "search_url": "https://sdmlib.sen.go.kr/sdmlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "시각"},
             {"name": "서울시교육청 양천도서관", "lat": 37.5234, "lng": 126.8521, "base_url": "https://yclib.sen.go.kr", "search_url": "https://yclib.sen.go.kr/yclib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰"},
             {"name": "서울시교육청 영등포평생학습관", "lat": 37.5261, "lng": 126.8954, "base_url": "https://ydpllc.sen.go.kr", "search_url": "https://ydpllc.sen.go.kr/ydpllc/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰글"},
             {"name": "서울시교육청 정독도서관", "lat": 37.5706, "lng": 126.9763, "base_url": "https://jdlib.sen.go.kr", "search_url": "https://jdlib.sen.go.kr/jdlib/intro/search/index.do?menu_idx=4&search_text={query}", "call_number_keyword": "큰글"} ]
            
# 도서 대출 가능 여부 및 책 정보 스크래핑
def scrape_library(book_title, library_name, base_url, search_url, call_number_keyword):
    url = search_url.format(query=book_title)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("div", class_="bookStateBar")
    book_data = []
    for book in books:
        try:
            img_container = book.find_previous('div', class_='thumb')
            if img_container:
                img_tag = img_container.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    img_url = img_tag['src']
                    if not img_url.startswith('http'):
                        img_url = base_url+ img_url
                else:
                    img_url = 'https://splib.sen.go.kr/resources/common/img/noImg.gif'
            else:
                img_url = 'https://splib.sen.go.kr/resources/common/img/noImg.gif'
            #책제목
            title_element = book.find_previous("a", class_="name goDetail")
            title = title_element.text.strip() if title_element else "제목 없음"
            #작가
            author_element = book.find_previous("dd", class_="author").find("span")
            author = author_element.text.strip() if author_element else "저자 없음"
            #큰글자 청구기호
            call_number_element = book.find_previous("dd", class_="data").find("span", string=lambda text: text and "청구기호" in text)
            call_number = call_number_element.text.split(": ")[-1].strip() if call_number_element else "청구기호 없음"
            #대출가능 여부 
            borrow_status_element = book.find("p", class_="txt")
            if borrow_status_element:
                borrow_status = borrow_status_element.get_text(strip=True)  
                borrow_status = re.sub(r'<.*?>', '', borrow_status) 
                borrow_status_ = "대출 가능" if "대출가능" in borrow_status else "대출 불가"
            else:
                borrow_status_ = "정보 없음"
            
            #함수 입력값 청구기호에 대해서 book_data 확장 
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
            print(f"오류 발생: {e}")
            continue
    return book_data

# 모든 도서관에서 scrape_library실행 
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

#사용자가 책 제목, 주소 입력 
book_title = input("도서 제목을 입력하세요: ")
user_address = input("사용자의 주소를 입력하세요: ")

books=get_books_from_all_libraries(book_title)
#책 이미지 데이터가 여러 도서관에 있을 경우, 젤 위의 도서관에서 가져오고, 책 이미지가 아무데도 존재하지 않으면 디폴트 값인 NoImage url을 불러옴 
if books:        
    selected_book=None
    default_img_url="https://splib.sen.go.kr/resources/common/img/noImg.gif"
    for book in books:
        if book["이미지"]!=default_img_url:
            selected_book=book
            break
    if selected_book is None:
        selected_book=books[0]
    print("\n검색된 도서 정보:")
    print(f"제목: {selected_book["제목"]}")
    print(f"{selected_book['저자']}")
    print(f"이미지: {selected_book['이미지']}")
    
    try:
        response=requests.get(selected_book["이미지"])
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.show()
        else:
            print("[이미지 로드 실패]")
    except Exception as e:
        print("[이미지 로드 오류]", e)
                
                 
    #사용자 위치 기반 위도 경도 반환 함수 호출하여 lat, lng 설정
    lat, lng = get_lat_lng(user_address, GOOGLE_MAPS_API_KEY)
    #모든 도서관에 대해서 사용자와의 거리 계산 
    if lat and lng:
        distances = []
        for library in libraries:
            distance = geodesic((lat, lng), (library["lat"], library["lng"])).km
            distances.append({"name": library["name"], "distance": distance, "base_url": library["base_url"],"lat":library["lat"],"lng":library["lng"]})

        distances.sort(key=lambda x: x["distance"])
        closest_libraries = distances[:3]
        print("\n도서 대출 상태:")
        for lib in closest_libraries:
            for book in books:
                if book['도서관'] == lib['name']:  # 도서관이 closest_libraries에 포함되어 있는지 확인
                    print(f"- [{book['도서관']}] 대출 상태: {book['대출 상태']}")
        print("\n가까운 도서관:")
        for lib in closest_libraries:
            print(f"- {lib['name']} (거리: {lib['distance']:.2f} km) - {lib['base_url']}")
    else:
        print("\n주소를 찾을 수 없습니다. 다시 입력해 주세요.")

    closest_libraries_map = [
                {
                    "name": lib["name"],
                    "distance": lib["distance"],
                    "url": lib["base_url"],
                    "lat": lib["lat"],  
                    "lng": lib["lng"]  
                }
    for lib in distances[:3]]
             
    def generate_html(lat, lng, closest_libraries_map):
        libraries_json = json.dumps(closest_libraries_map, ensure_ascii=False)
        html_content = f"""
                    <!DOCTYPE html>
                    <html lang="ko">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Google Maps API</title>
                        <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap" async defer></script>
                        <script>
                            function initMap() {{
                                var center = {{ lat: {lat}, lng: {lng} }};
                                var map = new google.maps.Map(document.getElementById('map'), {{
                                    zoom: 12,
                                    center: center,
                                    zoomControl: true,
                                    gestureHandling: "auto"
                                }});

                                var userMarker = new google.maps.Marker({{
                                    position: center,
                                    map: map,
                                    title: "사용자 위치",
                                    icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                                }});

                                var libraries = {libraries_json};  // 이미 필터링된 3개 도서관 사용

                                if (!Array.isArray(libraries) || libraries.length === 0) {{
                                    console.error("libraries 데이터가 없음!");
                                    return;
                                }}

                                let infoWindows = []; 

                                libraries.forEach(lib => {{
                                    console.log("마커 추가됨:", lib.name); 

                                    let marker = new google.maps.Marker({{
                                        position: {{ lat: lib.lat, lng: lib.lng }},
                                        map: map,
                                        title: lib.name,
                                        icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"  
                                    }});

                                    let infoWindow = new google.maps.InfoWindow({{
                                        content: `<strong>${{lib.name}}</strong><br>거리: ${{lib.distance.toFixed(2)}} km<br><a href="${{lib.url}}" target="_blank">도서관 홈페이지</a>`
                                    }});

                                    marker.addListener("click", function() {{
                                        infoWindows.forEach(win => win.close());
                                        infoWindow.open(map, marker);
                                        infoWindows.push(infoWindow);
                                    }});
                                }});
                            }}
                        </script>
                    </head>
                    <body>
                        <h2>가까운 도서관 지도</h2>
                        <div id="map" style="width: 100%; height: 500px;"></div>
                    </body>
                    </html>
                    """

        try: 
            file_name = "lib.html"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(html_content)
                  
        except Exception as e:
            print(f"파일 생성 중 오류 발생: {e}")

    generate_html(lat, lng, closest_libraries_map)

else:
    print("도서 제목과 주소를 모두 입력하세요!")
                    
