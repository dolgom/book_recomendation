from json_utils import load_json
from find_library.check_borrow import get_books_from_all_libraries
from find_library.location_utils import get_lat_lng, calculate_closest_libraries
from find_library.map_generator import generate_html
from PIL import Image
import requests
from io import BytesIO

GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # ← 실제 API 키 넣기

libraries = load_json('data/libraries.json')

book_title = input("도서 제목을 입력하세요: ")
user_address = input("당신의 주소를 입력하세요: ")

books = get_books_from_all_libraries(book_title, libraries)

if not books:
    print("도서 검색 결과가 없습니다.")
    exit()

# 대표 도서 하나 출력 + 이미지 표시
default_img = "https://splib.sen.go.kr/resources/common/img/noImg.gif"
selected_book = next((b for b in books if b["이미지"] != default_img), books[0])

print(f"\n제목: {selected_book['제목']}")
print(f"저자: {selected_book['저자']}")
print(f"이미지: {selected_book['이미지']}")

try:
    img_data = requests.get(selected_book["이미지"])
    img = Image.open(BytesIO(img_data.content))
    img.show()
except Exception as e:
    print("이미지 표시 오류:", e)

# 사용자 위치 → 위경도 변환
lat, lng = get_lat_lng(user_address, GOOGLE_MAPS_API_KEY)
if lat is None:
    print("주소를 인식하지 못했습니다.")
    exit()

closest = calculate_closest_libraries(lat, lng, libraries)

print("\n도서 대출 상태:")
for lib in closest:
    for book in books:
        if book["도서관"] == lib["name"]:
            print(f"- [{book['도서관']}] 대출 상태: {book['대출 상태']}")

print("\n가까운 도서관:")
for lib in closest:
    print(f"- {lib['name']} (거리: {lib['distance']:.2f} km)")

generate_html(lat, lng, closest, GOOGLE_MAPS_API_KEY)
