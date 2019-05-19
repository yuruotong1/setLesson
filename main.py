
import logger
import logging
import mycookie
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
        logging.info("进行入test_01")
        js2 = "var q=document.querySelector('#livetime_increase_0 > div.guide-bd.form.form--h > div.f-item.f-item-livetask > div > ul > li:nth-child(1) > div.ct-show > a').click()"
        js3='var q=document.querySelector("#livetime_increase_0 > div.guide-bd.form.form--h > div.f-item.f-item-livetask > div > ul > li:nth-child(1) > div.ct-edit > div > div.f-dates > i").click()'
        self.driver.execute_script(js3)

    def test_02(self):
        logging.info("进行入test_02")


if __name__ == '__main__':
    unittest.main()



