
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
        logging.info("执行完所有test")

        #cls.driver.quit()
    def test_01(self):
        # 获取课程总数
        #number = lesson.Lesson(self.driver).number()
        # 计算出第几周，每周上两节课
        #week = number
        # 查看第几周，星期几对应的日期
        #print(time.strptime('2019-1-1', '%Y-%U-%w').tm_mon)
        # 输入上课时间：先清空内容再输入
        #self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[166]/div[2]/div/div[1]/input').clear()
        #self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[166]/div[2]/div/div[1]/input').send_keys("2019-8-14")
        #点击课表的修改按钮
        #js4= 'var q=document.querySelector("#livetime_increase_0 > div.guide-bd.form.form--h > div.f-item.f-item-livetask > div > ul > li:nth-child(2) > div.ct-edit > div > div.f-dates > i").click()'
        #self.driver.execute_script(js4)
        lesson.Lesson(self.driver).weekArrangement({'星期五':('13:00','17:30')})



    def test_02(self):
        logging.info("进行入test_02")


if __name__ == '__main__':
    unittest.main()



