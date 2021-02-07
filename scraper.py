import time, os, io, re, json, logging, pickle, datetime
from seleniumwire import webdriver
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from urllib.request import urlretrieve
from google.cloud import vision
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class ScheduleUpdate:
    def __init__(self):
        logging.basicConfig(filename="error.log", level=logging.ERROR, format='%(asctime)s:%(name)s:%(message)s')

        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=SCOPES)
        if not os.path.exists("token.pkl"):
            self.credentials_OAuth = flow.run_console()
            pickle.dump(self.credentials_OAuth, open("token.pkl", "wb"))
        else:
            self.credentials_OAuth = pickle.load(open("token.pkl", "rb"))

        self.credentials = service_account.Credentials.from_service_account_file("auto-hub-v2-da28b62c34e1.json")
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)

        self.url = "https://collinsfoods.riteq.com.au/webess##login"

        self.chrome = webdriver.ChromeOptions()
        self.chrome.add_argument('--headless')
        self.chrome.add_argument('--disable-gpu')


        # Chrome Headless so no User Interface
        self.driver = webdriver.Chrome('chromedriver.exe', options=self.chrome)

        with open('credentials.json') as f:
            data = json.load(f)
        f.close()

        self.username = data[ "username" ]
        self.password = data[ "password" ]

        self.service = build('calendar', 'v3', credentials=self.credentials_OAuth)

        self.schedule = None
        self.code = None
        self.request = None

        self.work_list = []

        self.success = False


    def login(self):
        try:
            self.driver.get(self.url)

            time.sleep(5)

            img = self.driver.find_element_by_xpath('//*[@id="captchaImage"]')
            src = img.get_attribute('src')
            urlretrieve(src, "captcha.png")

            self.image_to_text()

            password_textbox = self.driver.find_element_by_xpath('//*[@id="UserName"]')
            password_textbox.send_keys(self.username)

            username_textbox = self.driver.find_element_by_xpath('//*[@id="Password"]')
            username_textbox.send_keys(self.password)

            code_textbox = self.driver.find_element_by_xpath('//*[@id="VerificationCode"]')
            code_textbox.send_keys(self.code)

            sign_in_button = self.driver.find_elements_by_xpath('// *[ @ id = "loginButton" ]')[ 0 ]
            sign_in_button.click()

            self.request = self.driver.wait_for_request("https://collinsfoods.riteq.com.au/WebEss/api/ScheduleApi/GetSchedulesWithRange")
            if self.request is not None:
                self.success = True
        except Exception as error:
            logging.error('URL:{} could not be reached. ERROR CODE: {}'.format(self.url, error))
            self.success = False


    def extract_schedule(self):
        try:
            self.schedule = json.loads(self.request.response.body.decode('utf-8'))

            self.success = True
        except Exception as error:
            logging.error(f'Schedule could not be extracted. ERROR CODE: {error}')
            self.success = False


    def get_events(self):
        now = datetime.datetime.utcnow().isoformat() + '+10:00'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=14, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [ ])
        for item in events:
            if item["summary"] == "Work":
                self.work_list.append(item)


    def input_to_calender(self):
        calender_add = []
        for day in self.schedule["ScheduleListModel"]:
            if day["IsViewable"]:
                check = True
                for event in self.work_list:
                    if day["StartTime"] + "+10:00" == event["start"]["dateTime"] and day["EndTime"] + "+10:00" == event["end"]["dateTime"]:
                        check = False
                if check:
                    calender_add.append(day)

        for day in calender_add:
            calender_request = {
                "start": {
                    "dateTime": (day["StartTime"] + "+10:00")
                },
                "end": {
                    "dateTime": (day["EndTime"] + "+10:00")
                },
                "colorId": 11,
                "summary": "Work"
            }
            self.service.events().insert(calendarId = "newmanbraydan@gmail.com", body = calender_request).execute()


    def image_to_text(self):
        file_name = os.path.abspath('captcha.png')

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        self.code = re.sub('[^0-9]', '', texts[0].description)


    def driver_exit(self):
        self.driver.quit()


    def complete_sequence(self):
        for j in range(6):
            self.login()
            if self.success:
                break
            time.sleep(5)
            if j > 5:
                self.driver_exit()
                return False

        if self.success:
            self.extract_schedule()
        else:
            return False
        if self.success:
            self.get_events()
            self.input_to_calender()
        else:
            return False
        if self.success:
            return True
        else:
            return False