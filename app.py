from flask import Flask, render_template, request, jsonify, session, redirect,send_file
from flask_restful import Api
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#↑사이트로 키값보내기
from selenium.webdriver.common.by import By
#↑위치에 따른 요소 가져올 때
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os, sys
import dialogflow
import uuid  # 세션아이디로 사용
import webbrowser
import cx_Oracle
from settings import config  # 프로젝트 아이디/API 키가 설정된 모듈 import
from settings.config import DIALOG_CONFIG

'''
pip install flask
pip install flask_restful
pip install flask_cors
pip install bs4
pip install requests
pip install cx_Oracle
pip install dialogflow
conda install selenium 

pip install xlrd
pip install openpyxl
//
pip install konlpy
pip install wordcloud
pip install stylecloud
//
pip install bing-image-downloader
'''

#Rest api요청을 처리할 클래스를 정의한 모듈 import
from api.petbook_list import PetBook
from api.petbook_items import PetBookItem
from api.pet_infomap import PetInfomap
from api.pet_wordcloud import PetCloud

#플라스크 앱 생성
app = Flask(__name__)
#JSON 응답 한글 처리
app.config['JSON_AS_ASCII'] = False
#챗봇
app.secret_key = 'asdqwe@asdqwe'
session_id = None
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = DIALOG_CONFIG['GOOGLE_APPLICATION_CREDENTIALS']


#CORS에러 처리
CORS(app)
#플라스크 앱을 인자로 하여 Api객체 생성:클래스와 URI매핑
api= Api(app)

#요청을 처리할 클래스와 요청 uri 매핑(라우팅)
#Api객체.add_resource(클래스명,'/요청url')
#api.add_resource(TodoList,'/todos')#get과 post구현 즉 전체 목록보기 와 추가기능
api.add_resource(PetBook,'/PetBook/<page>')
api.add_resource(PetBookItem,'/PetBookItem/<page>')
api.add_resource(PetInfomap,'/PetInfomap/<filename>')
api.add_resource(PetCloud,'/PetCloud/<search_word>')


@app.route('/requestFlask')
def onezero():
    key = request.args.get("param")
    dicResult={}
    img=[]
    href=[]
    title=[]
    content=[]

    print(key)
    try:
        # Headless Browser를 위한 옵션 설정
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        options.add_argument(
            'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')

        # 크롬드라이버(chromedriver.exe)가 위치한 경로 구하기
        driverPath = '{}\crawling\chromedriver.exe'.format(os.path.dirname(os.path.realpath(__file__)))

        # 1.WebDriver객체 얻기
        # 드라이버 생성시 두번 째 인자로 위에서 설정한 Headless브라우저로 띄우기 위한 옵션 전달
        driver = webdriver.Chrome(driverPath)
        #driver = webdriver.Chrome(driverPath,options=options)
        loot="https://search.naver.com/search.naver?where=post&sm=tab_jum&query="
        driver.get(loot)


        nameEC = EC.presence_of_element_located((By.NAME, 'query'))
        searchBox = WebDriverWait(driver, 3).until(nameEC)

        searchBox.send_keys(key)
        # Enter키를 누르기
        searchBox.send_keys(Keys.ENTER)


        # 블로그버튼 찾고 클릭처리하기
        blog_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#lnb > div > div.lnb_menu > ul > li.lnb3 > a > span')))
        blog_button.click()

        headers = {'User-Agent': 'Mozilla/5.0'}

        # 검색(1페이지)
        res = requests.get(
            loot+key,
            headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        blogImgs = soup.select('.sh_blog_thumbnail')
        blogHrefs = soup.select('.sh_blog_title')
        blogTitles = soup.select('.sh_blog_title')
        blogContents = soup.select('.sh_blog_passage')
        f=0
        for index in range(len(blogImgs)):
            img.append(blogImgs[index].get('src'))
            href.append(blogHrefs[index].get('href'))
            title.append(blogTitles[index].get('title'))
            content.append(blogContents[index].text)

        print("dicResult")
        print(dicResult)
        # 2페이지버튼 찾고 클릭처리하기
        twoPage_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#main_pack > div.paging > a:nth-child(2)')))
        twoPage_button.click()

        # 검색(2페이지)
        res = requests.get(
            "https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query=%EC%95%A0%EA%B2%AC%20%EB%8F%99%EB%B0%98%20%EC%B9%B4%ED%8E%98&sm=tab_pge&srchby=all&st=sim&where=post&start=11",
            headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        blogImgs = soup.select('.sh_blog_thumbnail')
        blogHrefs = soup.select('.sh_blog_title')
        blogTitles = soup.select('.sh_blog_title')
        blogContents = soup.select('.sh_blog_passage')

        for index in range(len(blogImgs)):
            img.append(blogImgs[index].get('src'))
            href.append(blogHrefs[index].get('href'))
            title.append(blogTitles[index].get('title'))
            content.append(blogContents[index].text)

        # 3페이지버튼 찾고 클릭처리하기
        twoPage_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#main_pack > div.paging > a:nth-child(4)')))
        twoPage_button.click()

        # 검색(3페이지)
        res = requests.get(
            "https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query=%EC%95%A0%EA%B2%AC%20%EB%8F%99%EB%B0%98%20%EC%B9%B4%ED%8E%98&sm=tab_pge&srchby=all&st=sim&where=post&start=21",
            headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        blogImgs = soup.select('.sh_blog_thumbnail')
        blogHrefs = soup.select('.sh_blog_title')
        blogTitles = soup.select('.sh_blog_title')
        blogContents = soup.select('.sh_blog_passage')

        for index in range(len(blogImgs)):
            img.append(blogImgs[index].get('src'))
            href.append(blogHrefs[index].get('href'))
            title.append(blogTitles[index].get('title'))
            content.append(blogContents[index].text)


        # 4페이지버튼 찾고 클릭처리하기
        twoPage_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#main_pack > div.paging > a:nth-child(5)')))
        twoPage_button.click()

        # 검색(4페이지)
        res = requests.get(
            "https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query=%EC%95%A0%EA%B2%AC%20%EB%8F%99%EB%B0%98%20%EC%B9%B4%ED%8E%98&sm=tab_pge&srchby=all&st=sim&where=post&start=31",
            headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        blogImgs = soup.select('.sh_blog_thumbnail')
        blogHrefs = soup.select('.sh_blog_title')
        blogTitles = soup.select('.sh_blog_title')
        blogContents = soup.select('.sh_blog_passage')

        for index in range(len(blogImgs)):
            img.append(blogImgs[index].get('src'))
            href.append(blogHrefs[index].get('href'))
            title.append(blogTitles[index].get('title'))
            content.append(blogContents[index].text)

        # 5페이지버튼 찾고 클릭처리하기
        twoPage_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#main_pack > div.paging > a:nth-child(5)')))
        twoPage_button.click()

        # 검색(5페이지)
        res = requests.get(
            "https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query=%EC%95%A0%EA%B2%AC%20%EB%8F%99%EB%B0%98%20%EC%B9%B4%ED%8E%98&sm=tab_pge&srchby=all&st=sim&where=post&start=41",
            headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        blogImgs = soup.select('.sh_blog_thumbnail')
        blogHrefs = soup.select('.sh_blog_title')
        blogTitles = soup.select('.sh_blog_title')
        blogContents = soup.select('.sh_blog_passage')

        for index in range(len(blogImgs)):
            img.append(blogImgs[index].get('src'))
            href.append(blogHrefs[index].get('href'))
            title.append(blogTitles[index].get('title'))
            content.append(blogContents[index].text)


    except TimeoutException as e:
        print('해당 페이지에 태그 요소가 존재하지 않거나, 해당 페이지가 3초동안 열리지 않았어요:', e)

    dicResult={"img": img, "href": href, "title": title, "content": content}
    print(dicResult);
    driver.close()
    return jsonify(dicResult)


#chatbot

@app.route('/')
def index():
    session['session_id'] = str(uuid.uuid4())

    return render_template('chatbot.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    responseData = request.get_json(force=True)
    ngrok = 'http://localhost:8080'

    yes_intent = ['응', '보여줘', '네', '알려줘', '알려주세요', '웅']
    no_intent = ['괜찮아', '아니']

    info = responseData['queryResult']
    pet = responseData['queryResult']['parameters']

    if 'action' in info:

        info = responseData['queryResult']['action']

        if responseData['queryResult']['queryText'] in yes_intent and info == 'Symptoms.Symptoms-yes':
            #webbrowser.open_new("http://localhost:8080/pettown/crawling/PetBookList.town?pageNum=339")
            reply = {"fulfillmentText": "궁금증이 해결 되었으면 좋겠어요!!@#$"+ngrok+"/pettown/crawling/PetBookList.town?pageNum=339"}

        elif responseData['queryResult']['queryText'] in yes_intent and info == 'FoodInfo.FoodInfo-yes':
            #webbrowser.open_new("http://localhost:8080/pettown/crawling/PetBookList.town?pageNum=342")
            reply = {"fulfillmentText": "궁금증이 해결 되었으면 좋겠어요!!@#$"+ngrok+"/pettown/crawling/PetBookList.town?pageNum=342"}

        elif responseData['queryResult']['queryText'] in yes_intent and info == 'CatWalk.CatWalk-yes':
            #webbrowser.open_new("http://localhost:8080/pettown/crawling/PetBookList.town?pageNum=275")
            reply = {"fulfillmentText": "궁금증이 해결 되었으면 좋겠어요!!@#$"+ngrok+"/pettown/crawling/PetBookList.town?pageNum=275"}

        elif responseData['queryResult']['queryText'] in yes_intent and info == 'petaction.petaction-yes':
            #webbrowser.open_new("http://localhost:8080/pettown/crawling/PetBookList.town?pageNum=264")
            reply = {"fulfillmentText": "궁금증이 해결 되었으면 좋겠어요!!@#$"+ngrok+"/pettown/crawling/PetBookList.town?pageNum=264"}

        elif responseData['queryResult']['queryText'] in yes_intent and info == 'fatcat.fatcat-yes':
            #webbrowser.open_new("http://localhost:8080/pettown/crawling/PetBookList.town?pageNum=314")
            reply = {"fulfillmentText": "날씬한 고양이가 되는 그날까지 화이팅!!!@#$"+ngrok+"/pettown/crawling/PetBookList.town?pageNum=314"}

        elif responseData['queryResult']['queryText'] in no_intent:
            reply = {"fulfillmentText": "궁금한점 있으면 또 물어봐주세요"}

    elif 'pet' in pet:
        pet = responseData['queryResult']['parameters']['pet']
        goods = responseData['queryResult']['parameters']['goods']

        if goods == '사료':
            if pet == '고양이':
                #webbrowser.open(url="http://localhost:8080/pettown/crawling/getRPList.do?rpType=food&rpKind=cat",new=0)
                reply = {"fulfillmentText": "고양이 사료 추천!!@#$"+ngrok+"/pettown/crawling/getRPList.do?rpType=food&rpKind=cat"}
            elif pet == '강아지':
                #webbrowser.open_new("http://localhost:8080/pettown/crawling/getRPList.do?rpType=food&rpKind=dog")
                reply = {"fulfillmentText": "강아지 사료 추천!!@#$"+ngrok+"/pettown/crawling/getRPList.do?rpType=food&rpKind=dog"}
        if goods == '장난감':
            if pet == '고양이':
                #webbrowser.open_new("http://localhost:8080/pettown/crawling/getRPList.do?rpType=toy&rpKind=cat")
                reply = {"fulfillmentText": "고양이 장난감 추천!!@#$"+ngrok+"/pettown/crawling/getRPList.do?rpType=toy&rpKind=cat"}
            elif pet == '강아지':
                #webbrowser.open_new("http://localhost:8080/pettown/crawling/getRPList.do?rpType=toy&rpKind=dog")
                reply = {"fulfillmentText": "강아지 장난감 추천!!@#$"+ngrok+"/pettown/crawling/getRPList.do?rpType=toy&rpKind=dog"}
    else:
        map = responseData['queryResult']['parameters']['map']
        area = responseData['queryResult']['parameters']['area']
        if map == '병원':
            if area == '금천구':
                #webbrowser.open_new("http://localhost:8080/pettown/InfoMap/InfoMap.hos?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B8%88%EC%B2%9C%EA%B5%AC")
                reply = {"fulfillmentText": "금천구 병원입니다!@#$"+ngrok+"/pettown/InfoMap/InfoMap.hos?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B8%88%EC%B2%9C%EA%B5%AC"}
            elif area == '강남구':
                #webbrowser.open_new("http://localhost:8080/pettown/InfoMap/InfoMap.hos?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B0%95%EB%82%A8%EA%B5%AC")
                reply = {"fulfillmentText": "강남구 병원입니다!@#$"+ngrok+"/pettown/InfoMap/InfoMap.hos?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B0%95%EB%82%A8%EA%B5%AC"}
            elif area == '마포구':
                #webbrowser.open_new("http://localhost:8080/pettown/InfoMap/InfoMap.hos?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EB%A7%88%ED%8F%AC%EA%B5%AC")
                reply = {"fulfillmentText": "마포구 병원입니다!@#$"+ngrok+"/pettown/InfoMap/InfoMap.hos?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EB%A7%88%ED%8F%AC%EA%B5%AC"}
        if map == '펫샵':
            if area == '금천구':
                #webbrowser.open_new("http://localhost:8080/pettown/InfoMap/InfoMap.shop?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B8%88%EC%B2%9C%EA%B5%AC")
                reply = {"fulfillmentText": "금천구 펫샵입니다!@#$"+ngrok+"/pettown/InfoMap/InfoMap.shop?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B8%88%EC%B2%9C%EA%B5%AC"}
            elif area == '강남구':
                #webbrowser.open_new("http://localhost:8080/pettown/InfoMap/InfoMap.shop?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B0%95%EB%82%A8%EA%B5%AC")
                reply = {"fulfillmentText": "강남구 펫샵입니다!@#$"+ngrok+"/pettown/InfoMap/InfoMap.shop?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B0%95%EB%82%A8%EA%B5%AC"}
            elif area == '마포구':
                #webbrowser.open_new("http://localhost:8080/pettown/InfoMap/InfoMap.shop?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EB%A7%88%ED%8F%AC%EA%B5%AC")
                reply = {"fulfillmentText": "마포구 펫샵입니다!@#$"+ngrok+"/pettown/InfoMap/InfoMap.shop?phaddress=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EB%A7%88%ED%8F%AC%EA%B5%AC"}

    return jsonify(reply)


def request_response_to_dialogflow(project_id, session_id, message, language_code):
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(project_id, session_id)

    if message:
        textInput = dialogflow.types.TextInput(text=message, language_code=language_code)
        queryInput = dialogflow.types.QueryInput(text=textInput)
        response = session_client.detect_intent(session=session_path, query_input=queryInput)

        return response.query_result.fulfillment_text


@app.route('/sendMessage', methods=['POST'])
def sendmessage():
    message = request.form['message']
    project_id = DIALOG_CONFIG['PROJECT_ID']

    fulfillment_text = request_response_to_dialogflow(project_id, session_id, message, 'ko')
    response_text = {"message": fulfillment_text}
    return jsonify(response_text)

#이미지 호출
@app.route('/wordcloud')
def get_image():
    filename = './petwordcloud.png'
    return send_file(filename, mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True,port=9292,host='0.0.0.0')
