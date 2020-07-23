from selenium import webdriver
import os,time,shutil
import cx_Oracle
from flask_restful import Resource
from flask import make_response



#1.Resource상속
class PetInfomap(Resource):
    #2.HTTP 메소드별 오버라이딩
    def __init__(self):
        pass

    #키값에 따른 데이타 하나 Select
    #get(self,매개변수)의 매개변수와 add_resource()의 <변수명>이 일치해야 한다
    #uri 매핑시 api.add_resource(클래스명,'/todos/<todo_id>')
    def get(self,filename):

        conn = cx_Oracle.connect(user='pet', password='pet', dsn='ghostiz.citqgkvtnwrm.ap-northeast-2.rds.amazonaws.com:1521/orcl')
        cursor = conn.cursor()

        try:
            # 파일 위치 url
            testUrl=None
            if filename == 'hospital':
                testUrl = "http://localdata.kr/datafile/each/02_03_01_P.xlsx"
            else:
                testUrl = "http://www.localdata.kr/datafile/each/02_03_06_P.xlsx"
            driverPath = '{}\chromedriver.exe'.format(os.path.dirname(os.path.realpath(__file__)))
            savePath = "C:\Document"
            newFilePath = './api/data/pet_'+filename+'.xlsx'

            options = webdriver.ChromeOptions()
            #options.add_argument('headless')
            options.add_argument("disable-gpu")
            options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

            options.add_experimental_option("prefs", {
                "download.default_directory": r"C:\Document",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
            #options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(driverPath, options=options)
            driver.set_window_size(1920, 1080)
            driver.get(testUrl)
            self.download_wait(savePath,driver)
            driver.quit()

            filename = max([savePath + '\\' + f for f in os.listdir(savePath)], key=os.path.getctime)
            print(filename)
            shutil.move(os.path.join(savePath, filename), newFilePath)

            import pandas as pd

            xlsx = pd.read_excel(newFilePath)
            print(xlsx.columns)
            # xlsx.dropna(how='any')
            # print(type(xlsx)) #<class 'pandas.core.frame.DataFrame'> 4470개가 나와야함
            xlsx = xlsx[:][['상세영업상태명', '사업장명', '도로명전체주소', '소재지전화', '좌표정보(X)', '좌표정보(Y)']]
            xlsx = xlsx.dropna(how='any', subset=['도로명전체주소', '사업장명', '좌표정보(X)', '좌표정보(Y)'])
            isNormal = xlsx['상세영업상태명'] == '정상'
            xlsx = xlsx[isNormal]
            xlsx = xlsx.fillna(value='')
            if len(xlsx) != 0:
                cursor.execute('DELETE PET_HOSPITAL')
            data = []
            for index in range(len(xlsx)):
                print('phNo:{},phName:{},phAddress:{}, phTel:{},phTmX:{},phTmY:{}'.format(index, xlsx.iloc[index, 1],
                                                                                          xlsx.iloc[index, 2],
                                                                                          xlsx.iloc[index, 3],
                                                                                          xlsx.iloc[index, 4],
                                                                                          xlsx.iloc[index, 5]))
                data.append([str(index),
                             xlsx.iloc[index, 1],
                             xlsx.iloc[index, 2],
                             xlsx.iloc[index, 3],
                             str(xlsx.iloc[index, 4]),
                             str(xlsx.iloc[index, 5])])

            cursor.executemany('INSERT INTO pet_hospital VALUES(:1,:2,:3,:4,:5,:6)', data)
            return str(len(xlsx))
        except Exception as e:
            print(e)
            return str(-1)
        finally:
            # commit
            conn.commit()
            # 자원 반납
            cursor.close()
            conn.close()
        #값을 json타입으로 만들어서 넘겨주기

    def download_wait(self,path_to_downloads,driver):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < 20:
            time.sleep(1)
            dl_wait = False
            for fname in os.listdir(path_to_downloads):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        return seconds