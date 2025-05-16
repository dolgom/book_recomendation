import streamlit as st
import os
import sys

# 상위 디렉토리를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    # Streamlit 앱 실행
    os.system("streamlit run streamlit_app/app.py") 