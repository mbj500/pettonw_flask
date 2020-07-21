from selenium import webdriver
import os,time,shutil
import cx_Oracle


testUrl = "http://www.localdata.kr/datafile/each/02_03_05_P.xlsx"
driverPath = '{}\chromedriver.exe'.format(os.path.dirname(os.path.realpath(__file__)))
savePath =  "C:\Document"
newFilePath = './data/pet_shop.xlsx'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR") # 한국어!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

options.add_experimental_option("prefs", {
  "download.default_directory": r"C:\Document",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome(driverPath, options=options)
driver.set_window_size(1920, 1080)
driver.get(testUrl)
time.sleep(7)
driver.quit()
filename = max([savePath + '\\' + f for f in os.listdir(savePath)], key=os.path.getctime)
shutil.move(os.path.join(savePath, filename), newFilePath)

import pandas as pd


conn = cx_Oracle.connect(user='pet',password='pet',dsn='localhost:1521/orcl')
cursor = conn.cursor()


xlsx = pd.read_excel(newFilePath)
print(xlsx.columns)
#xlsx.dropna(how='any')
#print(type(xlsx)) #<class 'pandas.core.frame.DataFrame'> 4470개가 나와야함
xlsx = xlsx[:][['상세영업상태명','사업장명','도로명전체주소','소재지전화','좌표정보(X)','좌표정보(Y)']]
xlsx = xlsx.dropna(how='any',subset=['도로명전체주소','사업장명','좌표정보(X)','좌표정보(Y)'])
isNormal = xlsx['상세영업상태명'] == '정상'
xlsx = xlsx[isNormal]
xlsx = xlsx.fillna(value='')
if len(xlsx) != 0:
    cursor.execute('DELETE PET_SHOP')
data=[]
for index in range(len(xlsx)):
    print('phNo:{},phName:{},phAddress:{}, phTel:{},phTmX:{},phTmY:{}'.format(index,xlsx.iloc[index,1],
                                                                              xlsx.iloc[index,2],
                                                                              xlsx.iloc[index,3],
                                                                              xlsx.iloc[index,4],
                                                                              xlsx.iloc[index,5]))
    data.append([str(index),
                 xlsx.iloc[index,1],
                 xlsx.iloc[index,2],
                 xlsx.iloc[index,3],
                 str(xlsx.iloc[index,4]),
                 str(xlsx.iloc[index,5])])

cursor.executemany('INSERT INTO pet_shop VALUES(:1,:2,:3,:4,:5,:6)', data)

#commit
conn.commit()
#자원 반납
cursor.close()
conn.close()

