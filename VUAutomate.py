from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import random
import config 

class VUautomate:
    totalquiz = 0
    totalassigemnt = 0
    subject = []
    nsubject = 0
    task = 0
    assigments = []
    def __init__(self, driver):
        self.driver = driver
    def is_alert_present(driver):
        try:
            driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False
    def checknotifications(element):
        try:
            element.find_element(By.XPATH, ".//*[starts-with(@id,'MainContent_gvCourseList_lblNotify')]")
            return True
        except NoSuchElementException:
            return False
        
    def login(self):
        url = 'https://vulms.vu.edu.pk/'
        # url = 'https://www.google.com'
        driver.get(url)
        try:
            user = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtStudentID"))
            )
        except:
            print('page failed to load ')
            exit()
        user.send_keys(config.STUDENT_ID) 
        for _ in range(2):
            time.sleep(1)
            password = driver.find_element(by=By.NAME,value='txtPassword')
            submit_button = driver.find_element(by=By.NAME, value='ibtnLogin')
            password.send_keys(config.STUDENT_PASSWORD) 
            submit_button.click()
            time.sleep(5)
            if VUautomate.is_alert_present(driver):
                print("Alert is present!")
                alert = driver.switch_to.alert
                alert.accept()
            # else:
                # print("No alert found.")
            time.sleep(2)
            if driver.current_url!=url:
                break
            print("Login Failed")
        if driver.current_url==url:
            print('stupid website')
            exit()
        
    def subnamehyperlnk(self):  
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f'MainContent_lblTitle')))
        elements = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-6')
        VUautomate.nsubject = len(elements)
        for element in elements:
            VUautomate.subject.append((element.find_element(By.CSS_SELECTOR, "h3.m-portlet__head-text").text).split('\n', 1)[0])
    def quiz(self):
        for i in range (VUautomate.nsubject):
            j=0
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f'MainContent_gvCourseList_hylnkQuizList_0')))
            elements = driver.find_elements(By.XPATH,"//*[starts-with(@id, 'MainContent_gvCourseList_hylnkQuizList_')]")
            if VUautomate.checknotifications(elements[i]):
                elements[i].click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, f'm-subheader__title'))) 
                elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'MainContent_gvTileRepeaterQuiz_pnl_')]")
                for element in elements:
                    check = element.find_elements(By.XPATH,"//*[starts-with(@id, 'MainContent_gvTileRepeaterQuiz_lblSubmitted_')]") 
                    deadline = element.find_elements(By.XPATH,"//*[starts-with(@id, 'MainContent_gvTileRepeaterQuiz_lblEndDate_')]")
                    print(check[j].text)
                    print('deadline ',deadline[j].text)
                    s = check[j].text
                    j+=1
                    if 'Submitted' not in s and s != '-':
                        VUautomate.totalquiz += 1
                driver.get('https://vulms.vu.edu.pk/home.aspx')
    def assigment(self):
        for i in range (VUautomate.nsubject):
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, f'MainContent_gvCourseList_hylnkAssignment_0')))
            elements = driver.find_elements(By.XPATH,"//*[starts-with(@id, 'MainContent_gvCourseList_hylnkAssignment_')]")
            if VUautomate.checknotifications(elements[i]):
                elements[i].click()
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, f'm-subheader__title'))) 
                elements = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'col-xs-9 col-sm-9 col-md-2 rightBorder pt-2 pb-3 pt-s-0 pb-s-')]")
                for element in elements:
                    s = element.text
                    if 'Submitted' not in s and s != '-':
                        VUautomate.totalassigemnt+= 1
                        VUautomate.assigments[i] += 1
                driver.get('https://vulms.vu.edu.pk/home.aspx')
    def solvequiz(self, frame,driver):
        take_quiz = driver.find_elements(By.XPATH,"//*[text()='Take Quiz']")
        driver.switch_to.default_content()
        if frame == 0:
            x=0
        elif frame == 2:
            x=1
        if len(take_quiz)==1:
            x=0

        take_quiz[x].click()
        time.sleep(2)

        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        for frame in enumerate(frames):
            try:
                driver.switch_to.frame(frame)
                element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, 'btnStartQuiz')))
                element.click()
                break  
            except:
                driver.switch_to.default_content()
                continue

        while True:
            time.sleep(5)
            driver.switch_to.default_content()
            elements = driver.find_elements(By.CSS_SELECTOR, "span[id^='lblRCompletionStatus']") 
            if 'Not' not in elements[self.task].text:
                print('done')
                break
            driver.switch_to.frame(frame)
            #EXTRACT TEXT FROM  QUIZ TO TEXT
            element = driver.find_element(By.XPATH, "//div[@id='divnoselect']")
            question_text = element.find_elements(By.TAG_NAME,'p')
            quiz_text = driver.find_elements(By.XPATH, "//*[contains(@id, 'lblExpression')]")
            combined_text = "\n".join(q_text.text for q_text in question_text)
            combined_text += "\n"
            combined_text += "\n".join(f"{i+1}. {element.text}" for i, element in enumerate(quiz_text))
            print(combined_text)

            rand = random.randint(0, len(quiz_text)-1)
            ans = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, f"radioBtn{rand}")))
            print('->',rand+1)
            time.sleep(2)
            ans.click()
            save = driver.find_element(By.ID, "btnSave")
            save.click()

            time.sleep(7)
            

        close_button=driver.find_elements(By.CSS_SELECTOR,"button.close")
        close_button[x].click()
        driver.switch_to.default_content()
    def completeclasses(self):
        next_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,f'a#lbtnNextLesson')))
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,f'a#lbtnPrevLesson'))).click()
        time.sleep(5)
        tabs = driver.find_elements(By.XPATH,"//a[starts-with(@id, 'tabHeader')]")
        elements = driver.find_elements(By.CSS_SELECTOR, "span[id^='lblRCompletionStatus']") 
        indexer = 0
        vindexer = 0
        print('tabs (len)',len(tabs))
        self.task = 0
        for i in tabs:
            
            if  'Pre-Assessment' in str(i.text):
                i.click()
                time.sleep(3)
                if 'Not' in elements[indexer].text:  
                    VUautomate.solvequiz(self,frame=0,driver=driver)
                indexer+=1
                self.task +=1
            elif 'Video' in str(i.text):
                while True:
                    i.click()
                    view = driver.find_elements(By.CSS_SELECTOR,"span[id^='lblVCompletionStatus']")
                    if 'Not' not in view[vindexer].text:
                        break
                    time.sleep(15)
                
                time.sleep(3)
            elif 'Post-Assessment' in str(i.text):
                i.click()
                time.sleep(3)
                if 'Not' in elements[indexer].text:
                    VUautomate.solvequiz(self,frame=2,driver=driver) 
                indexer+=1
                self.task +=1
            elif 'Reading' in str(i.text):
                i.click()
                time.sleep(10)
                indexer+=1
                self.task +=1
                # time.sleep(10)
        next_btn.click()


#
service = Service(config.PATH_TO_CHROME_DRIVER)

subject_index ='span#MainContent_gvCourseList_lblCurrentLessonNo_' 
selected_subject_index = subject_index+config.COURSE_INDEX

#
options = Options()
options.add_argument('--log-level=1')
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=service,options=options)
driver.maximize_window()
VUautomateor=VUautomate(driver=driver)



VUautomateor.login()
surveycheck=driver.current_url
if "survey.vu.edu.pk" in surveycheck:
    time.sleep(5)
    driver.find_element(By.XPATH,'//*[@id="imgbtnSkip"]').click() 
VUautomateor.subnamehyperlnk()
###
# select lecture
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,selected_subject_index)))
element.click()
###
while True:
    VUautomateor.completeclasses()
