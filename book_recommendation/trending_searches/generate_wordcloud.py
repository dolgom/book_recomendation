def generate_wordcloud(keywords, font_path="/System/Library/Fonts/Supplemental/AppleGothic.ttf"):
    import matplotlib.font_manager as fm
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    fm.fontManager.addfont(font_path)
    plt.rc('font', family='AppleGothic')

    text = " ".join(keywords)
    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color="white"
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("교보문고 실시간 인기 검색어 WordCloud")
    plt.show()
