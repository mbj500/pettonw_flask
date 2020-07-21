from bs4 import BeautifulSoup
import requests
from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import stylecloud
from flask_restful import Resource
from flask import make_response
import requests


#1.Resource상속
class PetCloud(Resource):
    #2.HTTP 메소드별 오버라이딩
    def __init__(self):

        self.title_list = []
        pass

    def get(self,search_word):
        self.search_word = search_word  # 검색어 지정
        self.get_titles(1, 30)

        return_text = self.make_wordcloud(120)

        return return_text


    def get_titles(self,start_num, end_num):
        # start_num ~ end_num까지 크롤링
        while 1:
            if start_num > end_num:
                break
            print(start_num)

            url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&start={}'.format(self.search_word,
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
                    self.title_list.append(title['title'])
            start_num += 10
        print(self.title_list)

    def make_wordcloud(self,word_count):
        twitter = Twitter()

        sentences_tag = []
        try:
            # 형태소 분석하여 리스트에 넣기
            for sentence in self.title_list:
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


            stylecloud.gen_stylecloud(text=dict(tags),
                                      background_color='#3A3547',
                                      font_path='C:\\Windows\\Fonts\\HANBatangB.ttf',
                                      icon_name="fas fa-dog",
                                      palette="colorbrewer.diverging.Spectral_11",
                                      gradient="horizontal",
                                      output_name="petwordcloud.png")
            return 'Success'
        except Exception as e:
            return 'Fail'


