import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trending_searches.keyword_scraper import get_kyobo_hot_keywords
from trending_searches.generate_wordcloud import generate_wordcloud

if __name__ == "__main__":
    keywords = get_kyobo_hot_keywords()
    if keywords:
        print("실시간 인기 검색어:")
        for i, kw in enumerate(keywords, 1):
            print(f"{i}. {kw}")
        generate_wordcloud(keywords)
    else:
        print("검색어 수집 실패")
