
import logger
import logging
import json


class MyCookie:
    def __init__(self,cookieUrl):
        self.cookieUrl=cookieUrl

    #从本地文件读取并设置cookie
    def setCookie(self,driver):
        logging.info("set Cookie in ./cookie/Cookie.txt")
        with open(self.cookieUrl, 'r', encoding='utf8') as f:
            self.listCookies = json.loads(f.read())
        for cookie in self.listCookies:
            driver.add_cookie(cookie)
        driver.refresh()
    #用于生成cookie
    def getCookie(self,driver):
        logging.info("save Cookie in ./cookie/Cookie.txt")
        dictCookies = self.driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        with open(self.cookieUrl, 'w') as f:
            f.write(jsonCookies)



