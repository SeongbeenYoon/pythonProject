#import
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
#큰 와일 문 안에 전체 코드를 넣어서 트라이 엑셉트 문을 사용해보자. 그리고 다른 곳에 클릭하고 새로 명령하기를 시켜보는 것도 괜찮지 않을까?
#실험이 필요해보이지만 우선 화요일을 무사히 넘기고 해야겠다
start = time.time()

#연도 하한선 설정
limit=int(input("limit year: "))
global to_config
to_config=[]
def remove_com(a):
    new_list=[]
    for v in a:
        if v not in new_list:
            new_list.append(v)
    return new_list
def remove_com_1(a):
    plag=0
    global to_config
    new_list=[]
    for v in a:
        if v not in new_list:
            new_list.append(v)
        else:
            to_config.append(a.index(v))
    return new_list
def remove_com_2(a):
    global to_config
    for i in range(len(a)):
        if(len(to_config)!=0):
            if (i == to_config[0]):
                a[i] = 0
                del to_config[0]
    for v in a:
        if(v==0):
            del v
    return a
#각각의 배열 선언
tags=[]
views=[]
scripts=[]
titles=[]
links=[]
years=[]

#보수를 고려한 초깃값
attempt=int(input("시도 횟수: ")) #시도 횟수 (최초 시도일 경우 0)
starting=1 #기본값, 코드 재시도시 입력받음
pagenum=1 #기본값, 코드 재시도시 입력받음
year=2021 #기본값, 코드 재시도시 입력받음
ecnt=0#시도 횟수


#코드 재시도시(에러로 인해 중단된 경우)
if(attempt>=1):
    # 이전 크롤링에서 끝난 위치의 정보가 담겨있음
    f_info = open('C:/Users/User/Desktop/tmp_info' + '_' + str(attempt - 1) + '.txt', 'rt', encoding='UTF8')
    while True:
        line=f_info.readline()
        if not line:
            break
        line=line.split("/")
        year=line[0]
        pagenum=line[1]
        starting=line[2]
    year=int(year)
    pagenum=int(pagenum)
    starting=int(starting)
    f_info.close()

#웹 드라이버 선언(firefox)
driver = webdriver.Firefox(executable_path="C:/Users/User/Downloads/geckodriver-v0.28.0-win64/geckodriver")

#웹 드라이버 실행
if(attempt==0):
    driver.get("https://www.ted.com/talks")

else:
    driver.get("https://www.ted.com/talks?page="+str(pagenum))
n = 0
iy = 0
wy = 0
ny = 0
e_plag=0
cstarting=0
while(year>=limit):
    try:
        while (year >= limit):
            print("erroris here 1")
            eplag=0
            # title, link, year 받는 부분
            cnt = starting
            wait = WebDriverWait(driver, 60)
            element_1 = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/ html / body / div[1] / div[2] / div "
                           "/ div[2] / div[2] / div[1] / div[" + str(
                    cnt) + "] / div / div / div / div[2] / h4[2] / a")))
            while (year >= limit and cnt <= 36):
                print("erroris here 2")
                dateinfo = element_1.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div[" + str(
                        cnt) + "]/div/div/div/div[2]/div/span/span").text
                linkinfo = element_1.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div["
                    + str(cnt) + "]/div/div/div/div[2]/h4[2]/a")
                title = linkinfo.text
                titles.append(title)
                link = linkinfo.get_attribute("href")
                links.append(link)
                ld = len(dateinfo)
                year = int(dateinfo[ld - 4:ld])
                print(year)
                years.append(year)
                cnt += 1
            print("페이지 마지막 영상의 연도: " + str(year))

            # for 문 내에서 각 영상의 script, tags, views 받아옴
            for i in range(starting, cnt):
                print("erroris here 3")
                cstarting=i
                e_plag=1
                print("영상 번호: " + str(pagenum) + "-" + str(i))
                n = i
                iy = ny + i
                wy = years[iy - starting]
                # 404error detect
                plagt = 0
                plags = 0
                plagv = 0

                # 반복문 실행시 임시 배열(초기화 역할 동시에)
                tag_one = []
                script_one = []

                # 영상 순차적으로 선택
                test_element = driver.find_element_by_xpath(
                    "/ html / body / div[1] / div[2] / div / div[2] "
                    "/ div[2] / div[1] / div[" + str(
                        i) + "] / div / div / div / div[2] / h4[2] / a")
                test_element.send_keys(Keys.ENTER)

                # 영상 대기
                try:
                    wait = WebDriverWait(driver, 60)
                    element_1 = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,
                         "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div[4]/div[1]/div/a")))
                except TimeoutException:
                    print("need another XPATH Wait for a while")
                    wait = WebDriverWait(driver, 10)
                    element_1 = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,
                         "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div[2]/div/div[4]/div[1]/div/a")))

                time.sleep(1)

                # 태그 받음
                try:
                    testtag = element_1.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div[4]/div[1]/div/a[1]")
                except NoSuchElementException:
                    plagt = 1
                else:
                    req = driver.page_source
                    soup = BeautifulSoup(req, 'html.parser')
                    tag = soup.select('meta[property = "og:video:tag"]')

                    for t in tag:
                        tc = t['content']
                        tag_one.append(tc)
                    tag_one.append(" ")
                    tags.append(tag_one)

                # 뷰 받음
                try:
                    testview = element_1.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div[4]/div[2]/section/div/div[2]/div/div[1]/span")
                except NoSuchElementException:
                    plagv = 1
                    views.append("No views")
                else:
                    view = element_1.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div[4]/div[2]/section/div/div[2]/div/div[1]/span").text
                    views.append(view)
                    print("check")

                print("태그뷰 완료", end=" ")

                # 스크립트 받음
                try:
                    testscr = element_1.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div[4]/div[1]/div/a[2]")
                except NoSuchElementException:
                    plags = 1
                    print("No Script")
                    scripts.append("No Scripts")

                else:
                    testscr.click()
                    time.sleep(3)
                    req = driver.page_source
                    soup = BeautifulSoup(req, 'html.parser')
                    divs = soup.findAll('div', {"class": "Grid__cell flx-s:1 p-r:4"})

                    temp = []
                    for d in divs:
                        scrs = d.findAll('p')
                        for s in scrs:
                            s = s.text
                            temp.append(s)
                    script_one = ''.join(temp)
                    if (len(script_one) == 0):
                        script_one = "No Scripts"
                    scripts.append(script_one)
                    print("스크립트 완료")

                temp_s=time.time()
                # 뒤로가기
                driver.back()
                if (plags == 0):
                    driver.back()
                ecnt = 0

            print("erroris here 4")
            starting = 1  # 보수시 starting 바뀜을 고려
            ny = len(years)
            # 다음 페이지로 넘김
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            tests = soup.find('div', {"class": "pagination"})
            num = len(tests.findAll('a'))
            element_1 = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/a[" + str(num) + "]")))
            testnext = element_1.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/a[" + str(num) + "]")
            testnext.send_keys(Keys.ENTER)
            pagenum += 1

            # for Refresh
            time.sleep(10)


    except:
        print("erroris here 5")
        if(ecnt<=5):
            ecnt += 1
            if(e_plag==1):
                year=wy
                starting=cstarting

            else:
                year=wy
                starting=n

        elif(ecnt>=5 and ecnt<=6):
            ecnt += 1
            driver.quit()
            time.sleep(5)
            driver.get("https://www.ted.com/talks?page=" + str(pagenum))
        else:
            print("Error did not fixed")
            break
#긁어온 데이터 분석해보니 약간 밀리는 뭔가가 있었던듯?
links=remove_com(links)
titles=remove_com_1(titles)
years=remove_com_2(years)

lens = [0, 0, 0, 0, 0, 0]
lens[0] = len(titles)
lens[1] = len(links)
lens[2] = len(years)
lens[3] = len(views)
lens[4] = len(tags)
lens[5] = len(scripts)
minlen = min(lens)
titles = titles[:minlen]
links = links[:minlen]
years = years[:minlen]
views = views[:minlen]
tags = tags[:minlen]
scripts = scripts[:minlen]

raw_data = {'titles': titles,
            'links': links,
            'years': years,
            'views': views,
            'tags': tags,
            'scripts': scripts
            }
raw_data = pd.DataFrame(raw_data)
raw_data.to_excel(excel_writer='C:/Users/User/Desktop/Data_' + str(attempt) + '.xlsx')
f_info = open('C:/Users/User/Desktop/tmp_info' + '_' + str(attempt) + '.txt', 'w', -1, "utf-8")
f_info.write(str(wy) + "/")
f_info.write(str(pagenum) + "/")
f_info.write(str(n) + "/")
f_info.close()
print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
