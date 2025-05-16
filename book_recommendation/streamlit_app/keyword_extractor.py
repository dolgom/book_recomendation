from typing import List
from kiwipiepy import Kiwi
from collections import Counter

def extract_keywords(text: str, num_keywords: int = 3) -> List[str]:
    """
    텍스트에서 키워드를 추출합니다.
    
    Args:
        text (str): 키워드를 추출할 텍스트
        num_keywords (int): 추출할 키워드 개수
        
    Returns:
        List[str]: 추출된 키워드 리스트
    """
    kiwi = Kiwi()
    
    # 명사 추출
    nouns = []
    for token in kiwi.analyze(text):
        if token.tag.startswith('NN'):  # 명사 태그
            nouns.append(token.form)
    
    # 가장 많이 등장하는 명사 추출
    counter = Counter(nouns)
    keywords = [word for word, _ in counter.most_common(num_keywords)]
    
    return keywords 