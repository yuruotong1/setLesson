
import logger
import logging
import mycookie
import lesson
from selenium import webdriver
import unittest
from selenium.webdriver.chrome.options import Options



class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome("./driver/chromedriver.exe", options=chrome_options)
        logger.Logger().getLog()
        #changeLessonPage = "https://ke.qq.com/agency/publish/index.html?cid=254956&term_id=100481009&cmd=p"
        #myCookie = mycookie.MyCookie('./cookie/Cookie.txt')
        #logging.info("ask changing lesson page：%s" % (changeLessonPage))
        #driver.get(changeLessonPage)
        #myCookie.setCookie(driver)
        cls.driver = driver

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_01(self):
        myLesson = lesson.Lesson(self.driver)
        #myLesson.setStartTime("2019-7-26")
        myLesson.setWeekArrangement({'星期5':('14:00','15:00'),'星期0':('15:00','18:00'),'星期1':('14:00','15:00')})
       # myLesson.lessonSchedule()
        myLesson.adjustmentLesson({'课程':'38','日期':'2019-5-25','时间':('5:00','6:00')})






if __name__ == '__main__':
    unittest.main()



