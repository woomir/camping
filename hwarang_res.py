from selenium import webdriver
import time
from bs4 import BeautifulSoup
import datetime

driver = webdriver.Chrome('/Users/WMHY/Downloads/chromedriver')

url = 'https://www.gyeongju.go.kr/hwarang/index.do'
driver.get(url)
time.sleep(1)

xpath = "/html/body/header/div/div/ul/li[2]/a"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.3)

xpath = "//input[@id='loginId']"
driver.find_element_by_xpath(xpath).send_keys("woomir")
time.sleep(0.1)

xpath = "//input[@id='loginPasswd']"
driver.find_element_by_xpath(xpath).send_keys("$52Telecast")
time.sleep(0.1)

xpath = "//button[@class='btnLogin']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.3)

driver.get("https://hwamyungcamping.com/reservation/real_time")
time.sleep(0.1)

driver.switch_to.alert.accept()
time.sleep(0.1)

# 2박으로 변경
xpath = "//option[@value='2']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.1)

driver.switch_to.alert.accept()
time.sleep(0.1)

# 달력 클릭 후 다음달로 넘기기
xpath = "//input[@id='resdate']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.1)
xpath = "//a[@data-handler='next']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.1)

# 정시가 되었을 때 그 이후의 코드 실행
nowTime = datetime.datetime.now().strftime('%H:%M:%S.%f')

while '00:00:00' not in nowTime:
    nowTime = datetime.datetime.now().strftime('%H:%M:%S.%f')
    time.sleep(0.5)
    print(nowTime)

# 선택한 날짜가 예약 가능한 상태인지 확인
repeatCount = 0
while repeatCount == 0:
    # 날짜 선택
    yourID = 'woomir'
    selectDay = '2021-05-30'
    extractionStr = selectDay[8:]
    url = 'https://hwamyungcamping.com/reservation/real_time?user_id=' + yourID + \
        '&site_id=&site_type=&dis_rate=0&user_dis_rate=&resdate=' + \
        selectDay + '&schGugun=2&price=0&bagprice=2000&allprice=0'
    driver.get(url)
    time.sleep(0.1)

    driver.switch_to.alert.accept()
    time.sleep(0.1)

    # 달력 클릭
    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    # 페이지 소스 읽기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    calendarInfoTd = soup.select('table.ui-datepicker-calendar>tbody>tr>td')

    # 선택한 날짜가 예약 가능한 상태인지 확인
    for i in range(0, len(calendarInfoTd)):
        text = calendarInfoTd[i].get_text()
        if extractionStr == text:
            possibleCheck = calendarInfoTd[i].select_one(
                'span.ui-state-default')
            if not possibleCheck:
                repeatCount = 1

siteNo = 'B1'
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
siteTotal = soup.select('a.cbtn')
count = 0
for text in siteTotal:
    count += 1
    if siteNo in text.get_text():
        if 'cbtn_on' in text.get('class'):
            xpath = "//*[@id='res_click_map']/div/a[" + str(count) + "]"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.1)
            xpath = "//a[@class='res_btn']"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.1)

            xpath = "//input[@name='car1']"
            driver.find_element_by_xpath(xpath).send_keys("68어4343")
            time.sleep(0.1)

            xpath = "//input[@name='car2']"
            driver.find_element_by_xpath(xpath).send_keys("말리부")
            time.sleep(0.1)

            xpath = "//a[@class='res_btn']"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.1)

            print('예약 성공!!')
        else:
            print('이미 예약된 자리입니다.')
