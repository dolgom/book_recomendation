import google.generativeai as genai
import json


def load_json(file_path):
    """JSON 파일 로드"""    
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

print('프로그램 시작')
books = load_json('data/filtered_tag/books_test.json')

api_key = 'AIzaSyCbXoQ0d210OC4jLntlwFBAG9nKoa__vWg'
genai.Client(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_book_recommendation(user_input):
    prompt = f"""
    다음은 책 제목과 책 소개 목록입니다:
    {json.dumps(books, ensure_ascii=False)}
    
    사용자 입력: {user_input}
    
    위 도서 목록에서 사용자의 관심사에 맞는 책을 3권 추천합니다.
    json파일에 들어있는 각 책의 카테고리들의 정보가 포함된 책에 대한 자세한 설명을 제공해주세요.
    정렬은 관심사가 높다고 판단된 순서대로 부탁합니다.
    각 추천은 다음 형식으로 제공해주세요:
    제목: [책의 제목]

    설명: [책에 대한 자세한 설명 (최대 200자)]
    """
    response = model.generate_content(prompt)
    return response.text

user_input = input('어떤 책을 찾고 계신가요? (예: 여행 관련 책 추천): ')

recommendation_list = get_book_recommendation(user_input)
print(recommendation_list)
