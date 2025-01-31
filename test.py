import streamlit as st
import requests
from bs4 import BeautifulSoup

def check_borrow_possible(search_title):
    url = 'https://splib.sen.go.kr/splib/intro/search/index.do?menu_idx=4&locExquery=111030&editMode=normal&officeNm=%EC%86%A1%ED%8C%8C%EB%8F%84%EC%84%9C%EA%B4%80&lectureNm=&mainSearchType=on&search_text=%ED%81%B0%EA%B8%80%EC%9E%90'
    params = {'search_text': search_title}
    
    results = [] # 대출가능 책 정보 저장 
    call_numbers = set() # 중복된 청구기호 제외하기 위함
    page = 1
    
    with st.spinner('검색 중...'):
                # 모든 페이지 순회
        while True:
            response = requests.get(url, params=params)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 도서 정보 찾기
            books = soup.find_all('div', class_='bookStateBar')

            for book in books:
                img_container = book.find_previous('div', class_='thumb')
                if img_container:
                    img_tag = img_container.find('img')
                    if img_tag and 'src' in img_tag.attrs:
                        img_url = img_tag['src']
                        if not img_url.startswith('http'):
                            img_url = 'https://splib.sen.go.kr/'+ img_url
                    else:
                        img_url = 'https://splib.sen.go.kr/resources/common/img/noImg.gif'
                else:
                    img_url = 'https://splib.sen.go.kr/resources/common/img/noImg.gif'

                title = book.find_previous('a', class_='name goDetail').text.strip()
                borrow_status = book.find('p', class_='txt').text.strip()
                call_number = book.find_previous('dd', class_='data').find('span', string=lambda text: '청구기호' in text)
            
                call_number = call_number.text.split(': ')[1].strip()
                if call_number not in call_numbers and '큰글' in call_number:
                    call_numbers.add(call_number)
                    
                    if search_title.lower() in title.lower():
                        if '대출가능' in borrow_status:
                            results.append({'title' : title, 'img_url' : img_url, 'borrow_status' : '대출가능'})
                        elif '예약초과' in borrow_status:
                            results.append({'title' : title, 'img_url' : img_url, 'borrow_status' : '대출불가(예약불가)'})
                        else:
                            results.append({'title' : title, 'img_url' : img_url, 'borrow_status' : '대출불가(예약가능)'})



                        
            next_button = soup.find('a', class_='paginate_button next')
            if not next_button:
                break
                
            page += 1
            
        return results if results else [f"{search_title} : 큰글자 도서를 찾을 수 없습니다"]



st.title('송파도서관 큰글자 도서 검색')

# 세션 상태 초기화
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False

user_input = st.text_input("검색할 도서 제목을 입력하세요:", key="search_input")

if user_input:
    search_results = check_borrow_possible(user_input)
    for result in search_results:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(result['img_url'], width=150)
        with col2:
            st.subheader(result['title'])
            st.markdown(f"<h3 style='font-size: 20px;'>{result['borrow_status']}</h3>", unsafe_allow_html=True)
            if result['borrow_status'] == '대출불가(예약불가)':
                st.write('5명예약중')
    st.session_state.search_performed = True
elif st.session_state.search_performed:
    st.session_state.search_performed = False
    st.experimental_rerun()
