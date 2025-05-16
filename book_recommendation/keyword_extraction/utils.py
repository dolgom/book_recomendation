
def load_stopwords(file_path="data/stopwords.txt"):
    """불용어 리스트 로드"""
    with open(file_path, "r", encoding="utf-8") as file:
        stopwords = set(line.strip() for line in file if line.strip())  # 빈 줄 제외
    return stopwords
