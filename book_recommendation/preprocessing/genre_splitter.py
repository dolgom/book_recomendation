import sys
import os

DATA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
sys.path.append(DATA_ROOT)

from json_utils import load_json, save_json
from tagging.utils import filtered_books_by_category, exclude_books_by_category, filtered_books_by_page


def literature_nonliterature_split():
    """문학/비문학 나눠 json파일로 저장"""
    books = load_json(os.path.join(DATA_ROOT), "filtered_tag/books_test.json") # 📌 데이터 수정(키워드 추출 완료 건으로)
    literature_books = filtered_books_by_category(books, ["소설/시/희곡", "에세이"])
    save_json(literature_books, "literature/literature.json")

    # 문학이 아닌 책들(non-literature) 저장
    non_literature_books = exclude_books_by_category(books, ["소설/시/희곡", "에세이"])
    save_json(non_literature_books, "non_literature/non_literature.json")

    print("완료")


# 문학
def literature_genre_split():
    """문학 데이터에서 장르별로 나누기"""
    literature_books = load_json("literature/literature.json") # 문학 데이터셋
    # 한국소설, 외국소설, 시/희곡, 고전문학, 상관없음, 에세이
    korea = filtered_books_by_category(literature_books, ['한국소설'], category_level=2)
    world = filtered_books_by_category(literature_books, ['영미소설', '중국소설', '러시아소설', '일본소설', '프랑스소설', '독일소설', '세계각국소설', '스페인/중남미소설', '북유럽소설'], category_level=2)
    poem = filtered_books_by_category(literature_books, ['시/희곡'], category_level=2)
    classic = filtered_books_by_category(literature_books, ['고전문학'], category_level=2)
    essay = filtered_books_by_category(literature_books, ['에세이'])

    save_json(korea, 'literature/literature_korea.json')
    save_json(world, 'literature/literature_world.json')
    save_json(poem, 'literature/literature_poem.json')
    save_json(classic, 'literature/literature_classic.json')
    save_json(essay, 'literature/literature_essay.json')

    print("문학 장르 완료")


def literature_volume_split():
    """문학 분량 별로 나누기"""
    literature_books = load_json("literature/literature.json")
    max_200 = filtered_books_by_page(literature_books, 200)
    max_300 = filtered_books_by_page(literature_books, 300)
    max_400 = filtered_books_by_page(literature_books, 400)
    max_500 = filtered_books_by_page(literature_books, 500)

    save_json(max_200, 'literature/literature_max_200.json')
    save_json(max_300, 'literature/literature_max_300.json')
    save_json(max_400, 'literature/literature_max_400.json')
    save_json(max_500, 'literature/literature_max_500.json')

    print("페이지 완료")


def literature_tag_split():
    """문학 분위기 태그 별로 나누기"""


# 비문학
# 인문 / 사회정치 / 예술 / 역사 / 경제경영 / 자기계발 / 건강취미 / 자연과학+IT모바일 / 청소년 / 가정살림 / 만화라노벨 / 상관없음
def non_literature_genre_split():
    """비문학 장르 별로 나누기"""
    non_literature_books = load_json('non_literature/non_literature.json')
    human = filtered_books_by_category(non_literature_books, ['인문'])
    social = filtered_books_by_category(non_literature_books, ['사회 정치'])
    art = filtered_books_by_category(non_literature_books, ['예술'])
    history = filtered_books_by_category(non_literature_books, ['역사'])
    economics = filtered_books_by_category(non_literature_books, ['경제 경영'])
    self = filtered_books_by_category(non_literature_books, ['자기계발'])
    healthy = filtered_books_by_category(non_literature_books, ['건강 취미'])
    science = filtered_books_by_category(non_literature_books, ['자연과학', 'IT 모바일'])
    young = filtered_books_by_category(non_literature_books, ['청소년'])
    house = filtered_books_by_category(non_literature_books, ['가정살림'])
    comics = filtered_books_by_category(non_literature_books, ['만화/라이트노벨'])

    save_json(human, 'non_literature/non_literature_human.json')
    save_json(social, 'non_literature/non_literature_social.json')
    save_json(art, 'non_literature/non_literature_art.json')
    save_json(history, 'non_literature/non_literature_history.json')
    save_json(economics, 'non_literature/non_literature_economics.json')
    save_json(self, 'non_literature/non_literature_self.json')
    save_json(healthy, 'non_literature/non_literature_healthy.json')
    save_json(science, 'non_literature/non_literature_science.json')
    save_json(young, 'non_literature/non_literature_young.json')
    save_json(house, 'non_literature/non_literature_house.json')
    save_json(comics, 'non_literature/non_literature_comics.json')
    print('비문학 장르 완료')


def non_literature_volume_split():
    """비문학 분량 별로 나누기"""
    non_literature_books = load_json("non_literature/non_literature.json")
    max_200 = filtered_books_by_page(non_literature_books, 200)
    max_300 = filtered_books_by_page(non_literature_books, 300)
    max_400 = filtered_books_by_page(non_literature_books, 400)
    max_500 = filtered_books_by_page(non_literature_books, 500)

    save_json(max_200, 'non_literature/non_literature_max_200.json')
    save_json(max_300, 'non_literature/non_literature_max_300.json')
    save_json(max_400, 'non_literature/non_literature_max_400.json')
    save_json(max_500, 'non_literature/non_literature_max_500.json')
    print('비문학 페이지 완료')
