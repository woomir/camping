from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import datetime


class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
#         options.add_argument('headless')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome(
            '/Users/WMHY/Downloads/chromedriver', options=options)

    def __call__(self):
        return self.driver

    def get_url(self, url):  # 새 창으로 url 열기
        self.driver.get(url)

    def get_default(self):  # default 프레임 이동
        while True:
            try:
                self.driver.switch_to_default_content()
                return
            except:
                print('default frame 이동')
                pass

    def get_fra(self, name):  # 특정 프레임 이동
        while True:
            try:
                self.driver.switch_to_frame(name)
                break
            except:
                self.get_default()
                print(name, 'frame 이동')
                continue

    def find_by_xpath(self, xpath):  # Xpath로 단일 요소 찾기
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                            (By.XPATH, xpath)))

    def find_by_class(self, class_name):  # class name으로 단일 요소 찾기
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                            (By.CLASS_NAME, class_name)))

    def find_by_tag(self, tag):  # tag로 단일 요소 찾기
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, tag)))

    def find_by_name(self, name):  # name으로 단일 요소 찾기
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.NAME, name)))

    def find_all_by_class(self, class_name):  # class name으로 모든 요소 찾기
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.TAG_NAME, class_name)))

    def find_all_by_tag(self, tag):  # tag로 모든 요소 찾기
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.TAG_NAME, tag)))

    def find_all_by_name(self, name):  # name으로 모든 요소 찾기
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.NAME, name)))

    def find_all_by_tag_with_obj(self, obj, name):  # tag으로 모든 요소 찾기
        return WebDriverWait(obj, 20).until(
            EC.presence_of_all_elements_located(
                (By.TAG_NAME, name)))

    def find_by_tag_with_obj(self, obj, name):  # tag으로 요소 찾기
        return WebDriverWait(obj, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, name)))

    def find_by_link(self, text):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, text)))

    def click(self, btn):
        self.driver.execute_script("arguments[0].click();", btn)

    def close(self):
        self.driver.close()


a = Driver()
# 화랑마을 홈페이지 접속
a.get_url('https://www.gyeongju.go.kr/hwarang/index.do')

# 로그인
a.find_by_xpath("/html/body/header/div/div/ul/li[2]/a").click()
# 아이디 입력
a.find_by_xpath("//input[@id='loginId']").send_keys("woomir")
# 비번 입력
a.find_by_xpath("//input[@id='loginPasswd']").send_keys("$52Telecast")
a.find_by_xpath("//button[@class='btnLogin']").click()

try:
    a.driver.switch_to.alert.accept()
except:
    print("경고창이 없습니다.")

# 예약 날짜에 해당하는 사이트로 이동 - 야영장
# a.get_url("https://www.gyeongju.go.kr/hwarang/page.do?step=list&mnu_uid=1997&tabNum=1&csi_uid=14&initYear=2021&initMonth=5&initDay=01&daynum=01")

# 정시가 되었을 때 그 이후의 코드 실행
nowTime = datetime.datetime.now().strftime('%H:%M:%S.%f')

while '00:00:00' not in nowTime:
    nowTime = datetime.datetime.now().strftime('%H:%M:%S.%f')
    time.sleep(0.5)
    print(nowTime)

check = 0
# 예약 날짜에 해당하는 사이트로 이동 - 육부촌
while check == 0:
    a.get_url("https://www.gyeongju.go.kr/hwarang/page.do?step=list&mnu_uid=1996&tabNum=1&csi_uid=12&initYear=2021&initMonth=7&initDay=31&daynum=31")
    try:
        a.driver.switch_to.alert.accept()
    except:
        check = 1

# 육부촌 자리 선택
# 301호
a.find_by_xpath("//a[@onclick='goReserve(111)']").click()
try:
    a.driver.switch_to.alert.accept()
except:
    print("경고창이 없습니다.")

# 401호
# a.find_by_xpath("//a[@onclick='goReserve(112)']").click()
# a.driver.switch_to.alert.accept()

# 501호
# a.find_by_xpath("//a[@onclick='goReserve(113)']").click()
# a.driver.switch_to.alert.accept()

# 주소 입력
a.find_by_xpath(
    "//input[@id='csr_address_0']").send_keys("부산시 해운대구 해운대로 469번길 110")
a.find_by_xpath("//input[@id='csr_address_1']").send_keys("106-304")

# 차량 번호 입력
a.find_by_xpath("//input[@class='csr_car']").send_keys("68어4343")

# 이용자 명단 입력
a.find_by_xpath("//input[@id='Addbtn']").click()

a.find_by_xpath("//input[@id='listName_1']").send_keys("진우민")
a.find_by_xpath("//select[@id='listGender_1']").send_keys("남")
a.find_by_xpath("//input[@id='listAge_1']").send_keys("40")

a.find_by_xpath("//input[@id='listName_2']").send_keys("정희영")
a.find_by_xpath("//select[@id='listGender_2']").send_keys("여")
a.find_by_xpath("//input[@id='listAge_2']").send_keys("41")

a.find_by_xpath("//input[@id='listName_3']").send_keys("진효성")
a.find_by_xpath("//select[@id='listGender_3']").send_keys("남")
a.find_by_xpath("//input[@id='listAge_3']").send_keys("8")

a.find_by_xpath("//input[@id='listName_4']").send_keys("진유성")
a.find_by_xpath("//select[@id='listGender_4']").send_keys("남")
a.find_by_xpath("//input[@id='listAge_4']").send_keys("5")

# 이용료 감면대상을 '해당사항 없음' 선택
a.find_by_xpath("//input[@id='reductionSubjectNo']").click()

# 예약 버튼 클릭
a.find_by_xpath("//button[@class='btn_ok']").click()
a.driver.switch_to.alert.accept()
