import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import telegram


def telegramSendMessage(month: str, week: int, siteNumber: int, camping: str):
    chat_token = "1752254532:AAHM8-RftUAr3V5KRJ2SzaBp41G8JTTeHIE"
    bot = telegram.Bot(token=chat_token)
    telegramMessageText = camping + ': ' + month + ' ' + str(week) + \
        '주차 토요일에 ' + str(siteNumber) + '개의 사이트가 생겼습니다.'
    bot.sendMessage(chat_id="-564369831", text=telegramMessageText)


webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')

driver = webdriver.Chrome(
    # '/home/ubuntu/chromedriver', options=webdriver_options) ## ubuntu
    '/Users/WMHY/Downloads/chromedriver', options=webdriver_options)  # masOs

# 대저 캠핑장
# =========================================================================
sendMessageCount = 0

while sendMessageCount == 0:

    url = 'https://www.daejeocamping.com/Camp.mobiz?camptype=camp01'
    driver.get(url)
    time.sleep(0.5)

    # Today를 기준으로 그 이후의 주말만 검색하기
    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    calendarInfoTd = soup.select('table.ui-datepicker-calendar>tbody>tr>td')
    tagNumber = 0
    _today = 1

    for tag in calendarInfoTd:
        tagNumber += 1
        if 'ui-datepicker-today' in tag['class']:
            _today = (tagNumber // 7) + 1

    # 이번달
    for i in range(_today, 5):

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)

        xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
            str(i)+"]/td[7]/a"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tagSelect = soup.select_one('div.reservationbox_wrap')
        aa = tagSelect.select('fieldset>input')
        count = 0
        for title in aa:
            if not title.has_attr("disabled"):
                count += 1

        if count > 0:
            telegramSendMessage('이번달', i, count, '대저캠핑장')
            print('대저캠핑장: 이번달 ' + str(i) + '주차에' + str(count) + '개 사이트 예약 가능')
            sendMessageCount += 1
        else:
            print('대저캠핑장: 이번달 ' + str(i) + '주차 변동없음')

    # 다음 달
    # nextMonthCount = []
    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    xpath = "//a[@data-handler='next']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    for i in range(1, 5):  # 토요일만 사이트 체크

        xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
            str(i)+"]/td[7]/a"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tagSelect = soup.select_one('div.reservationbox_wrap')
        aa = tagSelect.select('fieldset>input')
        count = 0
        for title in aa:
            if not title.has_attr("disabled"):
                count += 1

        if count > 0:
            telegramSendMessage('다음달', i, count, '대저캠핑장')
            print('대저캠핑장: 다음달 ' + str(i) + '주차에' + str(count) + '개 사이트 예약 가능')
            sendMessageCount += 1
        else:
            print('대저캠핑장: 다음달 ' + str(i) + '주차 변동없음')

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)

    # # 이번달로 다시 넘어가기
    # xpath = "//input[@id='resdate']"
    # driver.find_element_by_xpath(xpath).click()
    # time.sleep(0.1)
    # xpath = "//a[@data-handler='prev']"
    # driver.find_element_by_xpath(xpath).click()
    # time.sleep(0.1)
    # ==========================================================

    # 삼락 캠핑장
    url = 'http://www.nakdongcamping.com/reservation/real_time'

    driver.get(url)
    time.sleep(0.5)

    # 이번달
    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.select('table.ui-datepicker-calendar>tbody>tr>td')

    s = [6, 13, 20, 27, 34]

    for bb in s:
        weekNumber = s.index(bb) + 1

        if 'ui-state-disabled' not in res[bb]['class']:
            xpath = "//input[@id='resdate']"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.1)

            xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                str(weekNumber)+"]/td[7]"
            driver.find_element_by_xpath(xpath).click()

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
                telegramSendMessage('이번달', weekNumber, count, '삼락캠핑장')
                print('삼락캠핑장: 이번달 ' + str(weekNumber) +
                      '주차에' + str(count) + '개 사이트 예약 가능')
                sendMessageCount += 1
            else:
                print('삼락캠핑장: 이번달 ' + str(weekNumber) + '주차 변동없음')

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)

    # 다음 달
    xpath = "//a[@data-handler='next']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.select('table.ui-datepicker-calendar>tbody>tr>td')

    s = [6, 13, 20, 27, 34]

    for bb in s:
        weekNumber = s.index(bb) + 1

        if 'ui-state-disabled' not in res[bb]['class']:
            xpath = "//input[@id='resdate']"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.1)

            xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                str(weekNumber)+"]/td[7]"
            driver.find_element_by_xpath(xpath).click()

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
                telegramSendMessage('다음달', weekNumber, count, '삼락캠핑장')
                print('삼락캠핑장:다음달 ' + str(weekNumber) +
                      '주차에' + str(count) + '개 사이트 예약 가능')
                sendMessageCount += 1
            else:
                print('삼락캠핑장:다음달 ' + str(weekNumber) + '주차 변동없음')
    # 60초마다 실행
    time.sleep(10)
