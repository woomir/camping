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
    '/Users/WMHY/Downloads/chromedriver', options=webdriver_options)

# =========================================================================
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
        time.sleep(0.3)

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
                # print(title)
                siteInfo.append(title)
                count += 1

        if count > 0:
            telegramSendMessage('이번달', weekNumber, count, '삼락캠핑장')
            print('삼락캠핑장: 이번달 ' + str(weekNumber) +
                  '주차에' + str(count) + '개 사이트 예약 가능')
        else:
            print('삼락캠핑장: 이번달 ' + str(weekNumber) + '주차 변동없음')

    xpath = "//input[@id='resdate']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)

# 다음 달
xpath = "//a[@data-handler='next']"
driver.find_element_by_xpath(xpath).click()
time.sleep(0.3)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
res = soup.select('table.ui-datepicker-calendar>tbody>tr>td')

s = [6, 13, 20, 27, 34]

for bb in s:
    weekNumber = s.index(bb) + 1

    if 'ui-state-disabled' not in res[bb]['class']:
        xpath = "//input[@id='resdate']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.3)

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
        else:
            print('삼락캠핑장:다음달 ' + str(weekNumber) + '주차 변동없음')


# 텔레그램에서 그룹방 별 봇 아이디 확인 방법 (chat bot name: positioncheck), 그룹방 안에서 /start로 bot을 시작해줘야 함.
# chat_token = "1752254532:AAHM8-RftUAr3V5KRJ2SzaBp41G8JTTeHIE"
# chat = telegram.Bot(token=chat_token)
# updates = chat.getUpdates()
# for u in updates:
#     print(u.message['chat']['id'])
