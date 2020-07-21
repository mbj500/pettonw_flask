
from flask_restful import Resource
from flask import make_response
import requests


#1.Resource상속
class PetBook(Resource):
    #2.HTTP 메소드별 오버라이딩
    def __init__(self):
        pass
    def get(self,page):
        res = requests.get('https://petdoc.co.kr/ency/list?order=createdAt&page='+page+'&perPage=24&keyword=&needTotalCount=true')
        print(res.text)
        return make_response(res.text)
        #return TODOS[todo_id]

