
import logger
import logging
from selenium import webdriver
import json

LOG = logger.Logger(__name__).getLog()

class MyCookie:
    def __init__(self,cookieUrl):
        self.cookieUrl=cookieUrl
        logging.info("help me")

    #从本地文件读取并设置cookie
    def setCookie(self,driver):
        LOG.info("set Cookie in ./cookie/Cookie.txt")
        with open(self.cookieUrl, 'r', encoding='utf8') as f:
            self.listCookies = json.loads(f.read())
        for cookie in self.listCookies:
            driver.add_cookie(cookie)
        driver.refresh()
    #用于生成cookie
    def getCookie(self,driver):
        LOG.info("save Cookie in ./cookie/Cookie.txt")
        dictCookies = self.driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        with open(self.cookieUrl, 'w') as f:
            f.write(jsonCookies)

if  __name__ == '__main__':
    myCookie=MyCookie('./cookie/Cookie.txt')
    driver = webdriver.Chrome("./driver/chromedriver.exe")
    LOG.info("访问课程安排地址：https://ke.qq.com/agency/publish/index.html?cid=254956&term_id=100481009&cmd=p")
    driver.get("https://ke.qq.com/agency/publish/index.html?cid=254956&term_id=100481009&cmd=p")
    myCookie.setCookie(driver)

