import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import telegram
import random

# 텔레그램 메시지 전송 함수


def telegramSendMessage(month: str, day: str, siteNumber: int, camping: str, areaName: str):
    chat_token = "1752254532:AAHM8-RftUAr3V5KRJ2SzaBp41G8JTTeHIE"
    bot = telegram.Bot(token=chat_token)
    telegramMessageText = camping + ': ' + month + '월 ' + day + \
        '일 ' + areaName + '에 ' + str(siteNumber) + '개의 사이트가 있습니다.'
    bot.sendMessage(chat_id="-564369831", text=telegramMessageText)


def searchAreaSite(selectDay, thisMonth, areaName):
    siteFind = soup.select('a.num')
    activeSiteCount = 0
    for selectSatDay in selectDay:
        if len(selectSatDay) < 2:
            selectSatDay = '0'+selectSatDay
        searchDay = '2021-'+thisMonth+'-'+selectSatDay
        for active in siteFind:
            if searchDay in active['data-val']:
                if '예약가능' in active.select_one('img')['alt']:
                    activeSiteCount += 1
        if activeSiteCount > 0:
            telegramSendMessage('이번달', selectSatDay,
                                activeSiteCount, '진하캠핑장', areaName)
            print('진하캠핑장: ' + thisMonth + '월 ' + selectSatDay +
                  '일 ' + areaName + '에 ' + str(siteNumber) + '개 예약 가능')
            sendMessageCount += 1
        else:
            print('진하캠핑장: ' + thisMonth + '월 ' +
                  selectSatDay + '일 ' + areaName + '자리 없음.')


webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')

driver = webdriver.Chrome(
    # '/home/ubuntu/chromedriver', options=webdriver_options) ## ubuntu
    '/Users/WMHY/Downloads/chromedriver', options=webdriver_options)  # masOs

sendMessageCount = 0

sleepRandomTime = random.randrange(20, 40)
url = 'https://xn--om2bi2o9qdy7a48exzk3vf68fzzd.kr/'
driver.get(url)
time.sleep(0.5)
html = driver.page_source
if '/login?backURL=%2F' in html:
    # 로그인 화면으로 이동
    xpath = "//a[@href='/login?backURL=%2F']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    # 아이디 입력
    xpath = "//input[@id='m_id']"
    driver.find_element_by_xpath(xpath).send_keys('woomir@gmail.com')
    time.sleep(0.1)
    # 비번 입력
    xpath = "//input[@id='password']"
    driver.find_element_by_xpath(xpath).send_keys('$52Telecast')
    time.sleep(0.1)
    # 로그인 버튼 클릭
    xpath = "//button[@id='login_submit']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

# 예약사이트 접속
xpath = "//a[@href='/room/camping.php']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.2)
xpath = "//*[@id='wrap']/div[3]/div/ul/li[4]/a"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.1)

# 토요일 날짜 추출
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
satDay = soup.find_all('span', {'class': 'sat'})
satDayNumber = []
for text in satDay:
    if text.get_text() != '':
        satDayNumber.append(text.get_text())

# 몇월인지 확인
month = soup.find('div', {'class': 'month'})
monthNumber = month.find('em').get_text()
thisMonth = monthNumber[5:7]

# 반복 검색할 날짜 선택
selectDay = []
print('검색할 날짜를 선택하세요.(y로 대답하세요)')
for i in satDayNumber:
    answer = input(thisMonth+'월 ' + i + '일을 검색할까요?')
    if 'y' in answer:
        selectDay.append(i)
    elif 'n' in answer:
        print('ok')
    else:
        print('잘못 입력했어요.')

searchCount = 0
while sendMessageCount == 0:
    # 선택한 날짜에서 예약 가능한 A구역 Site 개수 파악
    dataValList = ['a', 'b', 'c', 'd', 'e', 'f']
    for area in dataValList:
        xpath = "//button[@data-val='" + area + "']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        areaName = soup.select_one("button.btn_active").get_text()
        searchAreaSite(selectDay, thisMonth, areaName)

    # 찾은 횟수 카운트
    searchCount += 1
    print('Searching : ' + str(searchCount) + '번째')

    # 30~60초 랜덤 실행
    time.sleep(sleepRandomTime)
