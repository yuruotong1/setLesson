
import logger
import logging
import mycookie
from selenium import webdriver




if  __name__ == '__main__':
    # 初始化log
    logger.Logger().getLog()
    # 初始化cookie
    myCookie=mycookie.MyCookie('./cookie/Cookie.txt')
    driver = webdriver.Chrome("./driver/chromedriver.exe")
    changeLessonPage ="https://ke.qq.com/agency/publish/index.html?cid=254956&term_id=100481009&cmd=p"
    driver.get(changeLessonPage)
    logging.info("ask changing lesson page：%s"%(changeLessonPage))
    # 设置cookie
    myCookie.setCookie(driver)

