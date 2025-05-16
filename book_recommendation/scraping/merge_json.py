import json
import glob

DATA_DIR = "../data/raw_scraped"
OUTPUT_FILE = f"{DATA_DIR}/final_books.json"

# JSON 파일 자동 검색
json_files = glob.glob(f"{DATA_DIR}/books_*.json")

all_books = []
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        all_books.extend(data)

# 최종 JSON 파일 저장
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_books, f, ensure_ascii=False, indent=4)

print(f"{OUTPUT_FILE}으로 최종 합침")
