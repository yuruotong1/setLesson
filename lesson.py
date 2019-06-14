
from datetime import datetime
from datetime import timedelta
import logging
import math
from selenium.webdriver.support.wait import WebDriverWait
class Lesson:
    def __init__(self,driver):
        self.driver = driver

    def totalLessonNumber(self):
        ul = self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul')
        lis = ul.find_elements_by_xpath('li')
        lessonNumber = len(lis)
        logging.info("课程总数是：%s"%(lessonNumber))
        return lessonNumber
    # setStartTIme设置直播开始日期，格式：年-月-日。比如2019-5-19
    # todo 可以根据第一节课的上课时间来定
    def setStartTime(self,startTime):
        logging.info("设置上课时间：%s" % (startTime))
        if type(startTime) !=datetime:
            startTime = datetime.strptime(startTime, '%Y-%m-%d')
        self.startTime = startTime
        openCalendar = self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[1]/div[1]/div/div[1]/i')
        openCalendar.click()
        currentTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[2]').text
        startTimeFormated = '%s年%s月'%(startTime.year,startTime.month)
        while  currentTime != startTimeFormated:
            currentTimeFormated = datetime.strptime(currentTime, '%Y年%m月')
            if currentTimeFormated < startTime:
                nextMonth =  self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[3]')
                nextMonth.click()
            elif currentTimeFormated > startTime:
                lastMonth = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[1]')
                lastMonth.click()
            currentTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[2]').text
        findStartTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/tbody//td[@data-date="%s/%s/%s"]'%(startTime.year,startTime.month,startTime.day))
        findStartTime.click()
    def getStartTime(self):
        return self.startTime

    # firstLessonCall 的作用是，调课时，要调的课通常不是第一节课，并且上一节课存在但没有编辑按钮（因为已经上过了）
    def clickEdit(self,currentLesson,firstLessonCall):
        # 点击编辑前要前确认上一个按钮没有完成按钮
        if currentLesson != 1 :
            WebDriverWait(self.driver, 3).until(
                lambda driver: self.driver.find_element_by_xpath(
                    '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[1]/a' % (currentLesson - 1)))
        js4 = 'var q= document.querySelector("#livetime_increase_0 > div.guide-bd.form.form--h > div.f-item.f-item-livetask > div > ul > li:nth-child(%s) > div.ct-show > a").click()' % (
            currentLesson)
        self.driver.execute_script(js4)
    def setSchoolTimeYearAndMonth(self,currentLesson,lastSchoolTime):
        self.driver.find_element_by_xpath(
            '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[1]/input' % (
                currentLesson)).clear()
        self.driver.find_element_by_xpath(
            '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[1]/input' % (
                currentLesson)).send_keys(lastSchoolTime.strftime("%Y-%m-%d"))
    def setSchoolTimeHourAndMin(self,currentLesson,currentSchoolTime):
        self.driver.find_element_by_xpath(
            '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[1]/div[1]/input' % (
                currentLesson)).clear()
        self.driver.find_element_by_xpath(
            '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[1]/div[1]/input' % (
                currentLesson)).send_keys(currentSchoolTime.strftime("%H:%M"))
    def setQuitTimeHourAndMin(self,currentLesson,currentSchoolTime):
        self.driver.find_element_by_xpath(
            '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[2]/div[1]/input' % (
                currentLesson)).clear()
        self.driver.find_element_by_xpath(
            '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[2]/div[1]/input' % (
                currentLesson)).send_keys(currentSchoolTime.strftime("%H:%M"))
    def clickSave(self,currentLesson):
        self.driver.find_element_by_xpath(
            '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/a[1]' % (currentLesson)).click()
        self.driver
    # currentLesson是课程号，yearAndMonth上课的年月日Y-M-D，schoolTime上课时间H:M，quitTime下课时间H:M
    def setLessonTime(self,currentLesson,yearAndMonth,schoolTime,quitTime):

        self.clickEdit(currentLesson)
        # 输入上课年-月-日
        self.setSchoolTimeYearAndMonth(currentLesson, yearAndMonth)
        # 设置上课时间
        self.setSchoolTimeHourAndMin(currentLesson, schoolTime)

        # 设置下课时间
        self.setQuitTimeHourAndMin(currentLesson, quitTime)
        # 点击保存
        self.clickSave(currentLesson)


    def adjustmentLesson(self):
        currentLesson = 0
        while(currentLesson != self.totalLessonNumber()):
            pass
            # todo 读取yaml，根据yaml的时间来调用setLessonTime函数安排课程
            currentLesson += 1









