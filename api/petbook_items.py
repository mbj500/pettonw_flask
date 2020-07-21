
from flask_restful import Resource
from flask import make_response
from bs4 import BeautifulSoup
import requests



#1.Resource상속
class PetBookItem(Resource):
    #2.HTTP 메소드별 오버라이딩
    def __init__(self):
        pass

    #키값에 따른 데이타 하나 Select
    #get(self,매개변수)의 매개변수와 add_resource()의 <변수명>이 일치해야 한다
    #uri 매핑시 api.add_resource(클래스명,'/todos/<todo_id>')
    def get(self,page):
        res = requests.get('https://petdoc.co.kr/ency/' + page)
        soup = BeautifulSoup(res.text, 'html.parser')
        content = soup.select_one('body > div.wrap > div._contents_root.container > div > div.content_inner > div')
        #print(content.select_one('div:nth-child(1)'))

        i=1
        contentList = []
        while(True):
            div = content.select_one('div:nth-of-type('+str(i)+')')
            print(div['class'])
            if div['class'][0] =='banner_box':
                print('banner_box if문 입장')
                break
            if i == 2:
                text = div.h2.text
                print(text)
            elif div['class'][0] =='img_area':
                text = div.img['src']
                print(text)
            else:
                text = div.p.text
                print(text)
            contentList.append(text)
            i+=1

        #값을 json타입으로 만들어서 넘겨주기
        return make_response({'data':contentList})
        #return TODOS[todo_id]

