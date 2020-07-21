
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★리뷰,썸네일 가져오기(강아지)

#목록 정보 가져오기
import requests
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os, random, time

import cx_Oracle

conn = cx_Oracle.connect(user='pet',password='pet',dsn='ghostiz.citqgkvtnwrm.ap-northeast-2.rds.amazonaws.com:1521/orcl')
cursor = conn.cursor()


#selenium
# Headless Browser를 위한 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')

# 크롬드라이버(chromedriver.exe)가 위치한 경로 구하기
driverPath = '{}\chromedriver.exe'.format(os.path.dirname(os.path.realpath(__file__)))
# 1.WebDriver객체 얻기
# 드라이버 생성시 두 번째 인자로 위에서 설정한 Headless브라우저로
# 띄우기 위한 옵션 전달
# driver = webdriver.Chrome(driverPath)
driver = webdriver.Chrome(driverPath, options=options)
#강아지 사료
driver.get('https://koozpetshop.com/category/%EA%B0%95%EC%95%84%EC%A7%80%EC%82%AC%EB%A3%8C/56/?cate_no=56&sort_method=7#Product_ListMenu')

headers = {'User-Agent':'Mozilla/5.0'}


res1 = requests.get("https://koozpetshop.com/category/%EA%B0%95%EC%95%84%EC%A7%80%EC%82%AC%EB%A3%8C/56/?cate_no=56&sort_method=7#Product_ListMenu",headers=headers)
soup = BeautifulSoup(res1.text,'html.parser')

#상품명
productNames = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.description > strong > a > span:nth-child(2)')
#내용&가격
productValues = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div.description > ul > li:nth-child(2) > span')
#이미지 링크(혹시 모르니 https:를 추가해줄 계획)
lis = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a > img')
#상품 링크 (https://koozpetshop.com를 앞에 추가해줘야 함)
links = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a')



def get_sumnail(url,count):
    #print('url:'+url)
    driver.get(url)
    # 리뷰 페이지 전체
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#prdReview > div > div.xans-element-.xans-product.xans-product-review')))
        # 뷰티플스프로 스크래핑하기
        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        stores = soup.find('tbody', class_='center')

        reviews = stores.find_all('a')


        for review in reviews:
            # print(li.text)
            print('[강아지사료 리뷰]:{},count:{}'.format(review.text, count))
            data = [count, review.text]
            cursor.execute('INSERT INTO RP_REVIEW(rpNo,rpReview) VALUES(:1,:2)', data)

    except Exception as e:
        print('게시물이 없습니다.')
    finally:
        # 썸네일 1,2,3
        thumbnail = soup.select('#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.xans-element-.xans-product.xans-product-addimage.listImg > ul > li > img')
        for thumb in thumbnail:
            print('[썸네일(사료)]:{},count:{}'.format(thumb.get('src'), count))
            data = [count, thumb.get('src')]
            cursor.execute('INSERT INTO RP_IMG(rpNo,rpThumbnail) VALUES(:1,:2)', data)

count = 1

details=[]
for link in links:
    href=link.attrs['href']
    #print("https://koozpetshop.com"+href)
    get_sumnail("https://koozpetshop.com"+href,count)
    count += 1



#강아지 장난감
driver.get('https://koozpetshop.com/category/%EC%9E%A5%EB%82%9C%EA%B0%90/88/?cate_no=88&sort_method=7#Product_ListMenu')

res1 = requests.get("https://koozpetshop.com/category/%EC%9E%A5%EB%82%9C%EA%B0%90/88/?cate_no=88&sort_method=7#Product_ListMenu",headers=headers)
soup = BeautifulSoup(res1.text,'html.parser')

#상품명
productNames = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.description > strong > a > span:nth-child(2)')
#내용&가격
productValues = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div.description > ul > li:nth-child(2) > span')
#이미지 링크(혹시 모르니 https:를 추가해줄 계획)
lis = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a > img')
#상품 링크 (https://koozpetshop.com를 앞에 추가해줘야 함)
links = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a')

def get_sumnail2(url,count):
    #print('url:'+url)
    driver.get(url)

    # 리뷰 페이지 전체
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#prdReview > div > div.xans-element-.xans-product.xans-product-review')))
        # 뷰티플스프로 스크래핑하기

        stores = soup.find('tbody', class_='center')

        reviews = stores.find_all('a')

        for review in reviews:
            #print(li.text)
            print('장난감 리뷰 for문')
            if not review.text==None:
                print('[강아지장난감 리뷰]:{},count:{}'.format(review.text, count))
                data = [count, review.text]
                cursor.execute('INSERT INTO RP_REVIEW(rpNo,rpReview) VALUES(:1,:2)', data)
                print('장난감 리뷰 뽑아옴')



    except Exception as e:
        print('게시물이 없습니다.')

    finally:
        thumbnail = soup.select(
            '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.xans-element-.xans-product.xans-product-addimage.listImg > ul > li > img')
        for thumb in thumbnail:
            print('[썸네일(장난감)]:{},count:{}'.format(thumb.get('src'), count))
            data = [count, thumb.get('src')]
            cursor.execute('INSERT INTO RP_IMG(rpNo,rpThumbnail) VALUES(:1,:2)', data)
            print('썸네일 뽑아옴')

count = 21

details=[]
for link in links:
    href=link.attrs['href']
    print("https://koozpetshop.com"+href)
    get_sumnail2("https://koozpetshop.com"+href,count)
    count += 1



#강아지 옷
driver.get('https://koozpetshop.com/category/%EC%9D%98%EB%A5%98%EC%95%85%EC%84%B8%EC%82%AC%EB%A6%AC/142/?cate_no=142&sort_method=7#Product_ListMenu')

res1 = requests.get("https://koozpetshop.com/category/%EC%9D%98%EB%A5%98%EC%95%85%EC%84%B8%EC%82%AC%EB%A6%AC/142/?cate_no=142&sort_method=7#Product_ListMenu",headers=headers)
soup = BeautifulSoup(res1.text,'html.parser')

#상품명
productNames = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.description > strong > a > span:nth-child(2)')
#내용&가격
productValues = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div.description > ul > li:nth-child(1) > span:nth-child(2)')
#이미지 링크(혹시 모르니 https:를 추가해줄 계획)
lis = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a > img')
#상품 링크 (https://koozpetshop.com를 앞에 추가해줘야 함)
links = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a')

def get_sumnail3(url,count):
    #print('url:'+url)
    driver.get(url)

    # 리뷰 페이지 전체
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#prdReview > div > div.xans-element-.xans-product.xans-product-review')))
        # 뷰티플스프로 스크래핑하기

        stores = soup.find('tbody', class_='center')

        reviews = stores.find_all('a')

        for review in reviews:
            #print(li.text)
            print('옷 리뷰 for문')
            if not review.text==None:
                print('[강아지옷 리뷰]:{},count:{}'.format(review.text, count))
                data = [count, review.text]
                cursor.execute('INSERT INTO RP_REVIEW(rpNo,rpReview) VALUES(:1,:2)', data)
                print('옷 리뷰 뽑아옴')



    except Exception as e:
        print('게시물이 없습니다.')

    finally:
        thumbnail = soup.select(
            '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.xans-element-.xans-product.xans-product-addimage.listImg > ul > li > img')
        for thumb in thumbnail:
            print('[썸네일(옷)]:{},count:{}'.format(thumb.get('src'), count))
            data = [count, thumb.get('src')]
            cursor.execute('INSERT INTO RP_IMG(rpNo,rpThumbnail) VALUES(:1,:2)', data)
            print('썸네일 뽑아옴')

count = 41

details=[]
for link in links:
    href=link.attrs['href']
    #print("https://koozpetshop.com"+href)
    get_sumnail3("https://koozpetshop.com"+href,count)
    count += 1

#commit
conn.commit()
#자원 반납
cursor.close()
conn.close()

