import streamlit as st
import requests
from bs4 import BeautifulSoup

def check_borrow_possible(search_title):
    url = 'https://splib.sen.go.kr/splib/intro/search/index.do'
    params = {
        'menu_idx': '4',
        'locExquery': '111030',
        'editMode': 'normal',
        'officeNm': '송파도서관',
        'lectureNm': '',
        'mainSearchType': 'on',
        'search_text': f'큰글자 {search_title}'
    }
    
    results = [] # 대출가능 책 정보 저장 
    call_numbers = set() # 중복된 청구기호 제외하기 위함
    page = 1
    
    with st.spinner('검색 중...'):
        # 모든 페이지 순회
        while True:
            response = requests.get(url, params=params)
            soup = BeautifulSoup(response.text, 'html.parser')
        
            # 모든 도서 정보 찾기
            book_items = soup.find_all('li')

            for item in book_items:
                try:
                    # 도서 정보 추출
                    title_elem = item.find('a', class_='name goDetail')
                    if not title_elem:
                        continue
                        
                    title = title_elem.text.strip()
                    
                    # 대출 상태 찾기
                    state_bar = item.find('div', class_='bookStateBar')
                    if not state_bar:
                        continue
                    borrow_status = state_bar.find('p', class_='txt').text.strip()
                    
                    # 청구기호 찾기
                    data_dd = item.find('dd', class_='data')
                    if not data_dd:
                        continue
                    call_number_elem = data_dd.find('span', string=lambda text: '청구기호' in text if text else False)
                    if not call_number_elem:
                        continue
                        
                    call_number = call_number_elem.text.split(': ')[1].strip()
                    
                    # 이미지 URL 찾기
                    image_url = ''
                    img_tag = item.find('img')
                    if img_tag and img_tag.get('src'):
                        image_url = img_tag['src']
                    
                    if call_number not in call_numbers and '큰글' in call_number:
                        call_numbers.add(call_number)
                        
                        if search_title.lower() in title.lower():
                            results.append({
                                'title': title,
                                'status': '대출 가능' if '대출가능' in borrow_status else '대출 불가능',
                                'image_url': image_url
                            })
                except Exception as e:
                    continue
                        
            next_button = soup.find('a', class_='paginate_button next')
            if not next_button:
                break
                
            page += 1
            
        return results if results else [{'title': f"{search_title} : 큰글자 도서를 찾을 수 없습니다", 'status': '', 'image_url': ''}]

def display_search_results(books: list):
    """
    검색 결과를 Streamlit에 표시합니다.
    """
    if not books:
        st.warning("검색 결과가 없습니다.")
        return
        
    for book in books:
        col1, col2 = st.columns([1, 3])
        with col1:
            if book['image_url']:
                try:
                    st.image(book['image_url'], width=150)
                except Exception as e:
                    st.write("이미지를 불러올 수 없습니다.")
        with col2:
            st.write(f"**{book['title']}**")
            if book['status']:
                st.write(f"**상태**: {book['status']}")
        st.write("---") 