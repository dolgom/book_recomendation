import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from json_utils import load_json

"""바로 stopwords에 추가하는 코드 추가"""
stopwords_path = 'data/sample_stop.txt'

with open(stopwords_path, 'r', encoding='utf-8') as f:
    existing_stopwords = set(line.strip() for line in f if line.strip())

# 📌 데이터 수정 필요 - 작가를 stop word에 추가해 키워드 추출 시 나오지 않게끔
# 문학 비문학 모두
books = load_json('data/word.json')
new_stopwords = set()
for book in books:
    author = book.get('author', '').strip()
    if author:
        new_stopwords.update(author.split())

words_to_add = new_stopwords - existing_stopwords
if words_to_add:
    with open(stopwords_path, 'a', encoding='utf-8') as f:
        for word in sorted(words_to_add):
            f.write(word + '\n')
    print('작가 이름 불용어 처리 완료')
else:
    print('작가 이름 없음')
