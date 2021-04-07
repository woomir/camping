import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import telegram
import random
import datetime


def telegramSendMessage(month: str, day: str, siteNumber: int, camping: str):
    chat_token = "1752254532:AAHM8-RftUAr3V5KRJ2SzaBp41G8JTTeHIE"
    bot = telegram.Bot(token=chat_token)
    telegramMessageText = camping + ': ' + month + ' ' + day + \
        '일 ' + str(siteNumber) + '개 예약 가능'
    bot.sendMessage(chat_id="-564369831", text=telegramMessageText)  # Official
    # bot.sendMessage(chat_id="1003456250", text=telegramMessageText)  # Test


webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')

driver = webdriver.Chrome(
    # '/home/ubuntu/chromedriver', options=webdriver_options)  # ubuntu
    '/Users/WMHY/Downloads/chromedriver', options=webdriver_options)  # macOs

# =========================================================================
url = 'http://www.nakdongcamping.com/reservation/real_time'

driver.get(url)
time.sleep(0.5)

todayDay = datetime.datetime.now().day

# Today를 기준으로 그 이후의 검색 가능한 주말 찾기
xpath = "//input[@id='resdate']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.1)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
thisCalendarInfoTd = soup.select('table.ui-datepicker-calendar>tbody>tr>td')

# 이번달
thisSatDay = []
for j in range(1, 36):
    if (j+1) % 7 == 0:
        satText = thisCalendarInfoTd[j].get_text()
        if '\xa0' not in satText:
            if int(satText) > todayDay:
                thisSatDay.append(satText)

# 이번달이 몇월인지 확인
thisMonth = soup.select_one('span.ui-datepicker-month').get_text()

# 다음달로 이동
xpath = "//a[@data-handler='next']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.1)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
nextCalendarInfoTd = soup.select('table.ui-datepicker-calendar>tbody>tr>td')

# 다음달이 몇월인지 확인
nextMonth = soup.select_one('span.ui-datepicker-month').get_text()

# 다음 달
nextSatDay = []
satOrder = [6, 13, 20, 27, 34]
for j in satOrder:
    satText = nextCalendarInfoTd[j].get_text()
    if '\xa0' not in satText:
        if 'ui-state-disabled' not in nextCalendarInfoTd[j]['class']:
            nextSatDay.append(satText)

xpath = "//a[@data-handler='prev']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.1)

# 이번달 반복 검색할 날짜 선택
thisSelectDay = []
nextSelectDay = []
print('검색할 날짜를 선택하세요.(y나 n으로 대답하세요)')
for i in thisSatDay:
    answer = input(thisMonth + i + '일을 검색할까요?')
    if 'y' in answer:
        thisSelectDay.append(i)
    elif 'n' in answer:
        print('ok')
    else:
        print('잘못 입력했어요.')

# 다음달 반복 검색할 날짜 선택
for i in nextSatDay:
    answer = input(nextMonth + i + '일을 검색할까요?')
    if 'y' in answer:
        nextSelectDay.append(i)
    elif 'n' in answer:
        print('ok')
    else:
        print('잘못 입력했어요.')

# 변수 설정
searchCount = 0
sendMessageCount = 0

while sendMessageCount == 0:
    sleepRandomTime = random.randrange(20, 40)
    # 이번달 검색
    for k in thisSelectDay:
        for title in thisCalendarInfoTd:
            if k in title.get_text():
                arayIndex = thisCalendarInfoTd.index(title)
                weekNumber = (arayIndex // 7) + 1
                dayNumber = (arayIndex % 7) + 1
                xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                    str(weekNumber) + "]/td[" + str(dayNumber) + "]/a"
                driver.find_element_by_xpath(xpath).click()
                time.sleep(0.2)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                tagSelect = soup.select('div.click_inner')
                activeSite = soup.find_all('a', 'cbtn_on')
                siteInfo = []
                count = 0

                for title in activeSite:
                    if "area_c" not in title["class"]:
                        siteInfo.append(title)
                        count += 1

                if count > 0:
                    telegramSendMessage(thisMonth, k, count, '삼락캠핑장')
                    print('삼락캠핑장: ' + thisMonth + ' ' + k +
                          '일 ' + str(count) + '개 예약 가능')
                    sendMessageCount += 1
                else:
                    print('삼락캠핑장: ' + thisMonth + ' ' + k + '일 자리 없음')

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)

    xpath = "//a[@data-handler='next']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    # 다음달 검색
    for k in nextSelectDay:
        for title in nextCalendarInfoTd:
            kLen = len(k)
            titleLen = len(title.get_text())
            if k in title.get_text() and kLen == titleLen:
                arayIndex = nextCalendarInfoTd.index(title)
                weekNumber = (arayIndex // 7) + 1
                dayNumber = (arayIndex % 7) + 1
                xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                    str(weekNumber) + "]/td[" + str(dayNumber) + "]/a"
                driver.find_element_by_xpath(xpath).click()
                time.sleep(0.2)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                tagSelect = soup.select('div.click_inner')
                activeSite = soup.find_all('a', 'cbtn_on')
                siteInfo = []
                count = 0

                for title in activeSite:
                    if "area_c" not in title["class"]:
                        siteInfo.append(title)
                        count += 1

                if count > 0:
                    telegramSendMessage(nextMonth, k, count, '삼락캠핑장')
                    print('삼락캠핑장: ' + nextMonth + ' ' + k +
                          '일 ' + str(count) + '개 예약 가능')
                    sendMessageCount += 1
                else:
                    print('삼락캠핑장: ' + nextMonth + ' ' + k + '일 자리 없음')

    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    # 찾은 횟수 카운트
    searchCount += 1
    print('Searching : ' + str(searchCount) + '번째')

    # 30~60초 랜덤 실행
    time.sleep(sleepRandomTime)
