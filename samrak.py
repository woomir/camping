import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import telegram
import random
import datetime
from telegramCustomFunc import telegramSendMessage
import platform

# 변수 설정
searchCount = 0
sendMessageCount = 0


def connectWebsite(driver):
    url = 'http://www.nakdongcamping.com/reservation/real_time'
    driver.get(url)
    time.sleep(0.5)


def weekendSearch(driver):
    # Today를 기준으로 그 이후의 검색 가능한 주말 찾기
    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.2)
    html = driver.page_source
    global samrakSoup
    samrakSoup = BeautifulSoup(html, 'html.parser')
    global samrakThisCalendarInfoTd
    samrakThisCalendarInfoTd = samrakSoup.select(
        'table.ui-datepicker-calendar>tbody>tr>td')


def thisMonth(todayDay):
    # 이번달
    global samrakThisSatDay
    samrakThisSatDay = []
    for j in range(1, 36):
        if (j+1) % 7 == 0:
            satText = samrakThisCalendarInfoTd[j].get_text()
            if '\xa0' not in satText:
                if int(satText) > todayDay:
                    samrakThisSatDay.append(satText)

    # 이번달이 몇월인지 확인
    global samrakThisMonth
    samrakThisMonth = samrakSoup.select_one(
        'span.ui-datepicker-month').get_text()


def nextMonth(driver):
    # 다음달로 이동
    xpath = "//a[@data-handler='next']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.2)
    html = driver.page_source
    samrakSoup = BeautifulSoup(html, 'html.parser')
    global samrakNextCalendarInfoTd
    samrakNextCalendarInfoTd = samrakSoup.select(
        'table.ui-datepicker-calendar>tbody>tr>td')

    # 다음달이 몇월인지 확인
    global samrakNextMonth
    samrakNextMonth = samrakSoup.select_one(
        'span.ui-datepicker-month').get_text()

    # 다음 달
    global samrakNextSatDay
    samrakNextSatDay = []
    satOrder = [6, 13, 20, 27, 34]
    for j in satOrder:
        satText = samrakNextCalendarInfoTd[j].get_text()
        if '\xa0' not in satText:
            if 'ui-state-disabled' not in samrakNextCalendarInfoTd[j]['class']:
                samrakNextSatDay.append(satText)

    xpath = "//a[@data-handler='prev']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.2)


def repeatDayQuestion():

    # 이번달 반복 검색할 날짜 선택
    global samrakThisSelectDay
    global samrakNextSelectDay
    samrakThisSelectDay = []
    samrakNextSelectDay = []
    print('검색할 날짜를 선택하세요.(y나 n으로 대답하세요)')
    for i in samrakThisSatDay:
        answer = input(samrakThisMonth + i + '일을 검색할까요?')
        if 'y' in answer:
            samrakThisSelectDay.append(i)
        elif 'n' in answer:
            print('ok')
        else:
            print('잘못 입력했어요.')

    # 다음달 반복 검색할 날짜 선택
    for i in samrakNextSatDay:
        answer = input(samrakNextMonth + i + '일을 검색할까요?')
        if 'y' in answer:
            samrakNextSelectDay.append(i)
        elif 'n' in answer:
            print('ok')
        else:
            print('잘못 입력했어요.')


def thisAndNextMonthSearch(driver):
    if not __name__ == "__main__":
        url = 'http://www.nakdongcamping.com/reservation/real_time'
        driver.get(url)
        time.sleep(0.5)
        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)

    # 이번달 검색
    for k in samrakThisSelectDay:
        for title in samrakThisCalendarInfoTd:
            if k in title.get_text():
                arayIndex = samrakThisCalendarInfoTd.index(title)
                weekNumber = (arayIndex // 7) + 1
                dayNumber = (arayIndex % 7) + 1
                xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                    str(weekNumber) + "]/td[" + str(dayNumber) + "]/a"
                driver.find_element_by_xpath(xpath).click()
                time.sleep(0.5)
                html = driver.page_source
                samrakSoup = BeautifulSoup(html, 'html.parser')
                tagSelect = samrakSoup.select('div.click_inner')
                activeSite = samrakSoup.find_all('a', 'cbtn_on')
                siteInfo = []
                count = 0

                for title in activeSite:
                    if "area_c" not in title["class"]:
                        siteInfo.append(title)
                        count += 1

                if count > 0:
                    telegramSendMessage(samrakThisMonth, k, count, '삼락캠핑장')
                    print('삼락캠핑장: ' + samrakTShisMonth + ' ' + k +
                          '일 ' + str(count) + '개 예약 가능')
                    global sendMessageCount
                    sendMessageCount += 1
                else:
                    print('삼락캠핑장: ' + samrakThisMonth + ' ' + k + '일 자리 없음')

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.2)

    xpath = "//a[@data-handler='next']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.2)

    # 다음달 검색
    for k in samrakNextSelectDay:
        for title in samrakNextCalendarInfoTd:
            kLen = len(k)
            titleLen = len(title.get_text())
            if k in title.get_text() and kLen == titleLen:
                arayIndex = samrakNextCalendarInfoTd.index(title)
                weekNumber = (arayIndex // 7) + 1
                dayNumber = (arayIndex % 7) + 1
                xpath = "//*[@id='ui-datepicker-div']/table/tbody/tr[" + \
                    str(weekNumber) + "]/td[" + str(dayNumber) + "]/a"
                driver.find_element_by_xpath(xpath).click()
                time.sleep(0.5)
                html = driver.page_source
                samrakSoup = BeautifulSoup(html, 'html.parser')
                tagSelect = samrakSoup.select('div.click_inner')
                activeSite = samrakSoup.find_all('a', 'cbtn_on')
                siteInfo = []
                count = 0

                for title in activeSite:
                    if "area_c" not in title["class"]:
                        siteInfo.append(title)
                        count += 1

                if count > 0:
                    telegramSendMessage(samrakNextMonth, k, count, '삼락캠핑장')
                    print('삼락캠핑장: ' + samrakNextMonth + ' ' + k +
                          '일 ' + str(count) + '개 예약 가능')
                    sendMessageCount += 1
                else:
                    print('삼락캠핑장: ' + samrakNextMonth + ' ' + k + '일 자리 없음')

        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.1)


if __name__ == '__main__':
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
