from bs4 import BeautifulSoup
import requests
from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import stylecloud

search_word = "반려동물"  # 검색어 지정
title_list = []


def get_titles(start_num, end_num):
    # start_num ~ end_num까지 크롤링
    while 1:
        if start_num > end_num:
            break
        print(start_num)

        url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&start={}'.format(search_word,
                                                                                                     start_num)
        req = requests.get(url)

        # 정상적인 request 확인
        if req.ok:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            # 뉴스제목 뽑아오기
            titles = soup.select(
                'ul.type01 > li > dl > dt > a'
            )

            # list에 넣어준다
            for title in titles:
                title_list.append(title['title'])
        start_num += 10
    print(title_list)


def make_wordcloud(word_count):
    twitter = Twitter()

    sentences_tag = []
    # 형태소 분석하여 리스트에 넣기
    for sentence in title_list:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-' * 30)

    print(sentences_tag)
    print('\n' * 3)

    noun_adj_list = []
    # 명사와 형용사만 구분하여 이스트에 넣기
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun', 'Adjective']:
                noun_adj_list.append(word)

    # 형태소별 count
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    print(tags)



    # WordCloud, matplotlib: 단어 구름 그리기
    #font_path = '/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf' font_path=font_path,
    '''
    wc = WordCloud(font_path='C:\\Windows\\Fonts\\HANBatangB.ttf', background_color='white', width=800, height=600)
    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10,8))
    plt.axis('off')
    plt.imshow(cloud)
    #plt.show()
    '''

    '''
    colors=['#ecf0f1', '#3498db', '#e74c3c'],
    '''

    stylecloud.gen_stylecloud(text=dict(tags),
                              background_color='#3A3547',
                              font_path='C:\\Windows\\Fonts\\HANBatangB.ttf',
                              icon_name="fas fa-dog",
                              palette="colorbrewer.diverging.Spectral_11",
                              gradient="horizontal",
                              output_name="/static/petwordcloud.png")

    '''
    # wordCloud생성
    # 한글꺠지는 문제 해결하기위해 font_path 지정
    wc = WordCloud(font_path=font, background_color='white', width=800, height=600)
    print(dict(tags))
    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()
    '''

    '''
    plt.savefig(
        os.path.join('results','wordcloud.png'),
        bbox_inches='tight',
        transparent=True,
        pad_inches=0.1
    )
    '''


if __name__ == '__main__':
    # 1~200번게시글 까지 크롤링
    get_titles(1, 200)

    # 단어 30개까지 wordcloud로 출력
    make_wordcloud(120)
