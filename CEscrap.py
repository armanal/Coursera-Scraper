import time
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import chrome
from selenium.webdriver.common.action_chains import ActionChains
#from selenium import selenium as sel


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

import pickle
import os.path
import getpass

###just some gi


########################################################################
class CSsc:
    """"""
    #----------------------------------------------------------------------
    def __init__(self, URL, CookieFile = 'coockies.pkl', ResumeFile = "dump.pkl"):
        """Constructor"""
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\Arman\Desktop\chromedriver_win32\chromedriver")
        self.mainWindow = self.browser.current_window_handle
        self.cookieFile = CookieFile
        self.resumeFlie = ResumeFile
        
        self.CourseURL = URL
        self.UsernameString = ''
        self.PasswordString = ''        

        self.browser.get(self.CourseURL)
        
        #cookies = openObj(self.cookieFile)
        #if cookies != None:
            #for cookie in cookies:
                #self.browser.add_cookie(cookie)
            #del cookies
            #self.browser.get(self.CourseURL)
            
        self.weeks = 0
        self.lessons = 0
        self.data = []        

        prevwork = openObj(self.resumeFlie)
        if prevwork != None:
            self.lessonList = prevwork
            self.weeks = self.lessonList[len(self.lessonList) - 1].weekNum + 1
            self.lessons = self.lessonList[len(self.lessonList) - 1].lessonNum + 1
        else:
            self.lessonList = []
        
        self.blocktime = 1
    
    #----------------------------------------------------------------------
    def LogIn(self):
        """"""
        print('trying logIn...')
        #self.browser.find_element_by_css_selector('#c-ph-right-nav > ul > li:nth-child(4) > a').click()
        #----------------------------------------------------------------------
        def lfreq():
            print("login form request")
            lg = self.waitForElement(locator=(By.LINK_TEXT, 'Log In'), time=20, tryes=2)
            if not lg == None:
                lg.click()
                return True
            return False
        #----------------------------------------------------------------------
        def fillf():
            print('wait for form')

            username = self.waitForElement((By.CSS_SELECTOR, 'div[data-state="login"] .c-user-modal-content form .c-user-modal-controls input#user-modal-email , #rendered-content div.rc-AuthenticationModal div.c-modal-content form > div.c-user-modal-controls input[type="email"]'), 6, 10)
            if not username == None:
                username.clear()
                username.send_keys(self.UsernameString)
            else:
                return False

            password = self.browser.find_element_by_css_selector('div[data-state="login"] .c-user-modal-content form .c-user-modal-controls input#user-modal-password , #rendered-content div.rc-AuthenticationModal div.c-modal-content form > div.c-user-modal-controls input[type="password"]')
            password.clear()
            password.send_keys(self.PasswordString)
            
            self.browser.find_element_by_css_selector('div[data-state="login"] .c-user-modal-content form button , #rendered-content div.rc-AuthenticationModal div.c-modal-content form button').click()

            print('form filled and sent')
            
            for i in range(0, 4):
                if not self.waitForLoad((By.CSS_SELECTOR, '#rendered-content div.rc-AuthenticationModal div.c-modal-content form button')):
                    self.browser.find_element_by_css_selector('#rendered-content div.rc-AuthenticationModal div.c-modal-content form button').click()
                else:
                    return True
                return False
        
        if lfreq():
            if fillf():
                #if self.waitForLoad((By.LINK_TEXT, 'Log In')):
                    #if not os.path.isfile(self.cookieFile):
                        #time.sleep(30)
                        #sevaObj(self.browser.get_cookies(), self.cookieFile)
                return True
        else:
            return True
        return False
    
    def courseEnroll(self):
        def al(driv):
            el = driv.find_element_by_css_selector('#rendered-content div.body-container div.rc-CTANavItem div.rc-CourseEnrollButton a')
            if el.get_attribute('href').endswith('#'):
                return False
            else:
                return True        
        try:   
            WebDriverWait(self.browser, 30).until(al,'')
            btn = self.browser.find_element_by_css_selector('#rendered-content div.body-container div.rc-CTANavItem div.rc-CourseEnrollButton a')
            self.browser.get(btn.get_attribute('href'))
        except:    
            print("\'go to course\' button not found. check CSS selector.\nor internet connection.")
    
    def main(self):
        #week = self.waitForElements((By.CSS_SELECTOR, '#rendered-content div.rc-OndemandApp div.rc-HomeLayoutBody main div.rc-HomePage div.rc-ReportCard div.rc-WeekRow'), 2, 30)
        
        self.waitForElement((By.CSS_SELECTOR, '#rendered-content div.rc-HomeLayoutBody > main > div > main > div.rc-Modal.box.rc-GleOnboardingModal > div.c-modal-content > div.button-container > button'), 2, 30).click()
        
        #self.waitForElement((By.CSS_SELECTOR, '#rendered-content div.rc-HomeLayoutBody > div.rc-Menu > div.menu div.rc-MainNavItem'), 2, 30).click()
        
        week = self.waitForElements((By.CSS_SELECTOR, '#rendered-content div.rc-HomeLayoutBody > div.rc-Menu > div.menu > ul.rc-FullMenuItems > li.rc-Drawer > ul.menu-drawer > li.module-list-item'), 2, 30)
        
        if week == None:
            print('failed to read weeks \n proccess terminated.')
            return None
        for w in range(self.weeks, len(week)):
            self.weeks = w
            #week = self.waitForElements((By.CSS_SELECTOR, '#rendered-content div.rc-OndemandApp div.rc-HomeLayoutBody main div.rc-HomePage div.rc-ReportCard div.rc-WeekRow'), 2, 30)
            week = self.waitForElements((By.CSS_SELECTOR, '#rendered-content div.rc-HomeLayoutBody > div.rc-Menu > div.menu > ul.rc-FullMenuItems > li.rc-Drawer > ul.menu-drawer > li.module-list-item'), 2, 30)
            
            time.sleep(self.blocktime)
            week[w].click()
            
            self.waitForElement((By.CSS_SELECTOR, '#rendered-content > div > div.rc-OndemandApp > div > div > div.rc-HomeLayoutBody > main > div > div.rc-PeriodPage > div.horizontal-box.wrap > div > section > div.rc-ModuleLessons > div > div > div > div:nth-child(1) > div > span:nth-child(2)'), 2, 30)
            lesson = self.waitForElements((By.CSS_SELECTOR, '#rendered-content main div.rc-ModuleLessons span.rc-ItemHonorsWrapper a i.cif-item-video, #rendered-content main div.rc-ModuleLessons span.rc-ItemHonorsWrapper a span.rc-CompletedItemIcon'))
            if lesson == None:
                print('failed to read lessons \n proccess terminated.')
                return None
            for l in range(self.lessons, len(lesson)):
                if l >= len(lesson):
                    break
                self.lessons = l
                self.waitForElement((By.CSS_SELECTOR, '#rendered-content > div > div.rc-OndemandApp > div > div > div.rc-HomeLayoutBody > main > div > div.rc-PeriodPage > div.horizontal-box.wrap > div > section > div.rc-ModuleLessons > div > div > div > div:nth-child(1) > div > span:nth-child(2)'), 1, 30)
                lesson = self.waitForElements((By.CSS_SELECTOR, '#rendered-content main div.rc-ModuleLessons span.rc-ItemHonorsWrapper a i.cif-item-video, #rendered-content main div.rc-ModuleLessons span.rc-ItemHonorsWrapper a span.rc-CompletedItemIcon.play'))
                time.sleep(self.blocktime)
                lesson[l].click()
                
                if self.waitForElement((By.CSS_SELECTOR, '#c-video_html5_api'), 2, 30) != None:
                    da = Lesson(self.CourseURL, w, l)
                    da.videoURL = self.browser.find_element_by_css_selector('#c-video_html5_api source[type="video/mp4"]').get_attribute('src')
                    #print(da.videoURL)
                    try:
                        da.subtitleURL = self.waitForElement((By.CSS_SELECTOR, '#rendered-content div.rc-LectureResources li.rc-SubtitleDownloadItem.resource-list-item a'), 1, 10).get_attribute('href')
                    except:
                        print("     no subtitle!")   
                    da.name = self.waitForElement((By.CSS_SELECTOR, '#rendered-content div.rc-OndemandApp div.week-drawer-container div.video-container div.c-video-title')).text.replace('-', ' ').replace('|', ' ').replace('\"',' ').replace('\'', ' ').replace(':', ' ').replace(',', ' ').replace(';', ' ').replace('?', '')
                    
                    self.lessonList.append(da)
                    print("{0} : {1}".format( w+1, l+1))
                    sevaObj(self.lessonList, 'dump.pkl')
                    
                
                self.browser.back()
            
            self.browser.back()
        if w > len(week):
            sevaObj(self.lessonList, 'data.obj')
            os.remove('dump.pkl')
        
        
    #----------------------------------------------------------------------    
    def waitForElement(self, locator, tryes = 1, time = 60):
        """"""
        for tryed in range(0 , tryes):
            try:
                elem = WebDriverWait(self.browser, time).until(EC.presence_of_element_located(locator))
                elem = WebDriverWait(self.browser, time).until(EC.visibility_of_element_located(locator))
                elem = WebDriverWait(self.browser, time).until(EC.element_to_be_clickable(locator))
                #elem = WebDriverWait(self.browser, time).until(EC.frame_to_be_available_and_switch_to_it(locator))
                return elem
            except:
                continue
        return None
    #----------------------------------------------------------------------    
    def waitForElements(self, locator, tryes = 1, time = 60):
        """"""
        for tryed in range(0 , tryes):
            try:
                WebDriverWait(self.browser, time).until(EC.presence_of_all_elements_located(locator))
                WebDriverWait(self.browser, time).until(EC.visibility_of_any_elements_located(locator))
                elem = self.browser.find_elements(locator[0], locator[1])
                #elem = WebDriverWait(self.browser, time).until(EC.element_to_be_clickable(elem[0]))
                return elem
            except:
                continue
        return None    
    #----------------------------------------------------------------------
    def waitForLoad(self, locator, duration = 60):
        """"""
        try:
            elem = self.browser.find_element(locator[0], locator[1])
        except:
            print('element missing!')
            return True
        Range = duration * 2
        for count in range(0, Range):  
            time.sleep(.5)
            try:
                elem == self.browser.find_element(locator[0], locator[1])
                elem == WebDriverWait(self.browser, .5).until(EC.visibility_of_element_located(locator))
                elem == WebDriverWait(self.browser, .5).until(EC.element_to_be_clickable(locator))
            except:
                return True    
        print("Timing out after {0} seconds and element is still there :-(".format(duration))
        return False       
            
        
                
            



########################################################################
class Lesson:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, CourseURL, WeekNum, LessonNum):
        """Constructor"""
        self.courseURL = CourseURL
        self.weekNum = WeekNum
        self.lessonNum = LessonNum
        
        self.name = ''
        self.videoURL = ''
        self.subtitleURL = ''
        self.slideURL = ''
    

#----------------------------------------------------------------------
def sevaObj(Obj, File):
    with open(File, 'wb') as file:
        pickle.dump(Obj, file, pickle.HIGHEST_PROTOCOL)
#----------------------------------------------------------------------
def openObj(File):
    if os.path.isfile(File):
        with open(File, 'rb') as file:
            Obj = pickle.load(file)
            return Obj
    return None



if __name__ == "__main__":
    l = True
    url = ''
    obj = None
    while(l):
        print('1. New course   2. Import last course to Internet Download Manager')
        print('3. Exit ')        
        if obj != None:
            print('4. Previous course   5. Change Coursers account')
        uin = input('->')
        if uin == '1':
            url = input('Enter Url of the course learn page\n[Ex:https://www.coursera.org/learn/data-structures] \n   :')
            obj = CSsc(url)
            obj.UsernameString = input('Username for Coursera account: ')
            obj.PasswordString = getpass.getpass('Password : ')
        if uin == '1' or uin == '4':
            print(obj.LogIn())
            obj.courseEnroll()
            obj.main()
        elif uin == '2':
            path = input('Enter the directory for the course to be downloaded : ')
            lessonList = openObj('data.obj')
            if lessonList == None:
                sys.exit(-1)
            
            for lesson in lessonList:
                name = str(lesson.lessonNum+1) + '.' + lesson.name
                if lesson.videoURL != '':
                    os.system('idman /a /n /p \"{0}\" /f \"{1}\" /d \"{2}\"'.format(path + "\\{0}".format(lesson.weekNum + 1) , name + ".mp4", lesson.videoURL))
                if lesson.subtitleURL != '':
                    os.system('idman /a /n /p \"{0}\" /f \"{1}\" /d \"{2}\"'.format(path + "\\{0}".format(lesson.weekNum + 1) , name + ".srt", lesson.subtitleURL))
                if lesson.slideURL != '':
                    os.system('idman /a /n /p \"{0}\" /f \"{1}\" /d \"{2}\"'.format(path + "\\{0}".format(lesson.weekNum + 1) , name + ".ppt", lesson.slideURL))
                print("{0} : {1}".format(lesson.weekNum+1, lesson.lessonNum+1))         
        elif uin == '3':
            l = False
        elif uin == '5':
            obj.UsernameString = getpass.getuser('Username for Coursera account: ')
            obj.PasswordString = getpass.getpass('Password : ')
    #Tested courses
    #https://www.coursera.org/learn/data-structures
    #https://www.coursera.org/learn/guitar/
    #https://www.coursera.org/learn/managingmoney
    #https://www.coursera.org/learn/big-data-graph-analytics/
    #https://www.coursera.org/learn/mobile-robot
    #https://www.coursera.org/learn/big-data-introduction
    #https://www.coursera.org/learn/optimizing-web-search
    #https://www.coursera.org/learn/seo-fundamentals
    #https://www.coursera.org/learn/basic-statistics
    #https://www.coursera.org/learn/web-app
    #https://www.coursera.org/learn/algorithms-on-graphs/
    #https://www.coursera.org/learn/linear-regression-model
    #https://www.coursera.org/learn/agile-team-management
    
    time.sleep(1)