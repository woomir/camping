import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import telegram
import random
import datetime
from telegramCustomFunc import telegramSendMessage
import platform

searchCount = 0
sendMessageCount = 0


def connectWebsite(driver):
    url = 'https://www.daejeocamping.com/Camp.mobiz?camptype=camp01'
    driver.get(url)
    time.sleep(0.5)


def weekendSearch(driver):
    # Today를 기준으로 그 이후의 검색 가능한 주말 찾기
    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    html = driver.page_source
    global daejeoSoup
    daejeoSoup = BeautifulSoup(html, 'html.parser')
    global daejeoThisCalendarInfoTd
    daejeoThisCalendarInfoTd = daejeoSoup.select(
        'table.ui-datepicker-calendar>tbody>tr>td')


def thisMonth(todayDay):
    # 이번달
    global daejeoThisSatDay
    daejeoThisSatDay = []
    for j in range(1, 36):
        if (j+1) % 7 == 0:
            satText = daejeoThisCalendarInfoTd[j].get_text()
            if '\xa0' not in satText:
                if int(satText) > todayDay:
                    daejeoThisSatDay.append(satText)
    # 이번달이 몇월인지 확인
    global daejeoThisMonth
    daejeoThisMonth = daejeoSoup.select_one(
        'span.ui-datepicker-month').get_text()


def nextMonth(driver):
    # 다음달로 이동
    xpath = "//a[@data-handler='next']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    html = driver.page_source
    daejeoSoup = BeautifulSoup(html, 'html.parser')
    global daejeoNextCalendarInfoTd
    daejeoNextCalendarInfoTd = daejeoSoup.select(
        'table.ui-datepicker-calendar>tbody>tr>td')

    # 다음달이 몇월인지 확인
    global daejeoNextMonth
    daejeoNextMonth = daejeoSoup.select_one(
        'span.ui-datepicker-month').get_text()

    # 다음 달
    global daejeoNextSatDay
    daejeoNextSatDay = []
    satOrder = [7, 14, 21, 28, 35]
    for j in satOrder:
        satText = daejeoNextCalendarInfoTd[j-1].get_text()
        if '\xa0' not in satText:
            weekOrder = j / 7
            xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                str(weekOrder) + "]/td[7]/a"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.1)
            html = driver.page_source
            daejeoSoup = BeautifulSoup(html, 'html.parser')
            tagSelect = daejeoSoup.select_one('div.reservationbox_wrap')
            aa = tagSelect.select('fieldset.ui-state-none')
            if len(aa) == 0:
                daejeoNextSatDay.append(satText)
            xpath = "//input[@id='resdate']"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.1)

    xpath = "//a[@data-handler='prev']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)


def repeatDayQuestion():
    # 이번달 반복 검색할 날짜 선택
    global daejeoThisSelectDay
    global daejeoNextSelectDay
    daejeoThisSelectDay = []
    daejeoNextSelectDay = []
    print('검색할 날짜를 선택하세요.(y나 n으로 대답하세요)')
    for i in daejeoThisSatDay:
        answer = input(daejeoThisMonth + i + '일을 검색할까요?')
        if 'y' in answer:
            daejeoThisSelectDay.append(i)
        elif 'n' in answer:
            print('ok')
        else:
            print('잘못 입력했어요.')

    # 다음달 반복 검색할 날짜 선택
    for i in daejeoNextSatDay:
        answer = input(daejeoNextMonth + i + '일을 검색할까요?')
        if 'y' in answer:
            daejeoNextSelectDay.append(i)
        elif 'n' in answer:
            print('ok')
        else:
            print('잘못 입력했어요.')


def thisAndNextMonthSearch(driver):
    if not __name__ == "__main__":
        url = 'https://www.daejeocamping.com/Camp.mobiz?camptype=camp01'
        driver.get(url)
        time.sleep(0.5)
        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)

    # 이번달 검색
    for k in daejeoThisSelectDay:
        for title in daejeoThisCalendarInfoTd:
            if k in title.get_text():
                arayIndex = daejeoThisCalendarInfoTd.index(title)
                weekNumber = (arayIndex // 7) + 1
                dayNumber = (arayIndex % 7) + 1

                xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                    str(weekNumber) + "]/td[" + str(dayNumber) + "]/a"
                driver.find_element_by_xpath(xpath).click()
                time.sleep(0.2)
                html = driver.page_source
                daejeoSoup = BeautifulSoup(html, 'html.parser')
                tagSelect = daejeoSoup.select_one('div.reservationbox_wrap')
                aa = tagSelect.select('fieldset>input')
                count = 0
                for bb in aa:
                    if not bb.has_attr("disabled"):
                        count += 1

                if count > 0:
                    telegramSendMessage(daejeoThisMonth, k, count, '대저캠핑장')
                    print('대저캠핑장: ' + daejeoThisMonth + ' ' +
                          k + '일 ' + str(count) + '개 예약 가능')
                    global sendMessageCount
                    sendMessageCount += 1
                else:
                    print('대저캠핑장: ' + daejeoThisMonth + ' ' + k + '일 자리 없음')

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)

    xpath = "//a[@data-handler='next']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

    # 다음달 검색
    for k in daejeoNextSelectDay:
        for title in daejeoNextCalendarInfoTd:
            kLen = len(k)
            titleLen = len(title.get_text())
            if k in title.get_text() and kLen == titleLen:
                arayIndex = daejeoNextCalendarInfoTd.index(title)
                weekNumber = (arayIndex // 7) + 1
                dayNumber = (arayIndex % 7) + 1

                xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                    str(weekNumber) + "]/td[" + str(dayNumber) + "]/a"
                driver.find_element_by_xpath(xpath).click()
                time.sleep(0.2)
                html = driver.page_source
                daejeoSoup = BeautifulSoup(html, 'html.parser')
                tagSelect = daejeoSoup.select_one('div.reservationbox_wrap')
                aa = tagSelect.select('fieldset>input')
                count = 0
                for bb in aa:
                    if not bb.has_attr("disabled"):
                        count += 1

                if count > 0:
                    telegramSendMessage(daejeoNextMonth, k, count, '대저캠핑장')
                    print('대저캠핑장: ' + daejeoNextMonth + ' ' +
                          k + '일 ' + str(count) + '개 예약 가능')
                    sendMessageCount += 1
                else:
                    print('대저캠핑장: ' + daejeoNextMonth + ' ' + k + '일 자리 없음')

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)


if __name__ == "__main__":
    # 사용자 컴퓨터 OS 확인 후 설정값 반환
    systemOS = platform.system()
    pathChromedriver = ''

    if systemOS == "Darwin":
        pathChromedriver = '/Users/WMHY/Downloads/chromedriver'
    elif systemOS == "Windows":
        pathChromedriver = ''
    elif systemOS == "Linux":
        pathChromedriver = '/home/ubuntu/chromedriver'

    webdriver_options = webdriver.ChromeOptions()
    webdriver_options .add_argument('headless')

    driver = webdriver.Chrome(pathChromedriver, options=webdriver_options)

    # 오늘 날짜 확인
    todayDay = datetime.datetime.now().day

    connectWebsite(driver)
    weekendSearch(driver)
    thisMonth(todayDay)
    nextMonth(driver)
    repeatDayQuestion()

    # 빈사이트 찾기 반복
    while sendMessageCount == 0:
        sleepRandomTime = random.randrange(20, 40)

        thisAndNextMonthSearch(driver)

        # 찾은 횟수 카운트
        searchCount += 1
        print('Searching : ' + str(searchCount) + '번째')

        # 30~60초 랜덤 실행
        time.sleep(sleepRandomTime)
