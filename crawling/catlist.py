#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★상품 가져오기(고양이)

#목록 정보 가져오기
import requests
import urllib
from bs4 import BeautifulSoup

import cx_Oracle

conn = cx_Oracle.connect(user='pet',password='pet',dsn='ghostiz.citqgkvtnwrm.ap-northeast-2.rds.amazonaws.com:1521/orcl')
cursor = conn.cursor()


headers = {'User-Agent':'Mozilla/5.0'}

#고양이 사료
res1 = requests.get("https://koozpetshop.com/category/%EA%B3%A0%EC%96%91%EC%9D%B4%EC%82%AC%EB%A3%8C/59/?cate_no=59&sort_method=7#Product_ListMenu",headers=headers)
soup = BeautifulSoup(res1.text,'html.parser')
#상품명
productNames = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.description > strong > a > span:nth-child(2)')
#내용&가격
productValues = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div.description > ul > li:nth-child(2) > span')
#이미지 링크(혹시 모르니 https:를 추가해줄 계획)
lis = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a > img')
#상품 링크 (https://koozpetshop.com를 앞에 추가해줘야 함)
links = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a')

count =61;
for li,name,price,link in zip(lis,productNames,productValues,links):
    print('[고양이사료]번호:{}, {}:\\{}원, 이미지:{}, 상품링크:{}, 종류:{}, 구분:{}'.format(count,name.text,price.text,li.get('src'),link.get('href'),'cat','food'))
    data = [count, li.get('src'), name.text, price.text, link.get('href'), 'cat', 'food']
    cursor.execute('INSERT INTO RECOMMEND_PRODUCT(rpNo,rpImg,rpTitle,rpContent,rpLink,rpKind,rpType) VALUES(:1,:2,:3,:4,:5,:6,:7)',data)
    count +=1


#고양이 장난감
res1 = requests.get("https://koozpetshop.com/category/%EA%B3%A0%EC%96%91%EC%9D%B4%EC%9E%A5%EB%82%9C%EA%B0%90/193/?cate_no=193&sort_method=7#Product_ListMenu",headers=headers)
soup = BeautifulSoup(res1.text,'html.parser')
#상품명
productNames = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.description > strong > a > span:nth-child(2)')
#내용&가격
productValues = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div.description > ul > li:nth-child(2) > span')
#이미지 링크(혹시 모르니 https:를 추가해줄 계획)
lis = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a > img')
#상품 링크 (https://koozpetshop.com를 앞에 추가해줘야 함)
links = soup.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li >  div.thumbnail > a')

count =81;
for li,name,price,link in zip(lis,productNames,productValues,links):
    print('[고양이장난감]번호:{}, {}:\\{}원, 이미지:{}, 상품링크:{}, 종류:{}, 구분:{}'.format(count,name.text,price.text,li.get('src'),link.get('href'),'cat','toy'))
    data = [count, li.get('src'), name.text, price.text, link.get('href'), 'cat', 'toy']
    cursor.execute('INSERT INTO RECOMMEND_PRODUCT(rpNo,rpImg,rpTitle,rpContent,rpLink,rpKind,rpType) VALUES(:1,:2,:3,:4,:5,:6,:7)',data)
    count +=1

#고양이 옷
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

count =101;
for li,name,price,link in zip(lis,productNames,productValues,links):
    print('[고양이옷]번호:{}, {}:\\{}원, 이미지:{}, 상품링크:{}, 종류:{}, 구분:{}'.format(count,name.text,price.text,li.get('src'),link.get('href'),'cat','cloth'))
    data = [count, li.get('src'), name.text, price.text, link.get('href'), 'cat', 'cloth']
    cursor.execute('INSERT INTO RECOMMEND_PRODUCT(rpNo,rpImg,rpTitle,rpContent,rpLink,rpKind,rpType) VALUES(:1,:2,:3,:4,:5,:6,:7)',data)
    count +=1



#commit
conn.commit()
#자원 반납
cursor.close()
conn.close()




