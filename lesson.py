
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
    # lessonPeriod 以字典形式给出，{'星期几':'上课时间',...},0代表星期日，6代表星期6。比如{'星期5':('14:00','15:00'),'星期0':('15:00','18:00')}
    def setWeekArrangement(self,lessonPeriod):
        self.lessonPeriod = lessonPeriod

    # 设置一周上几节课
    def weekLessonNumber(self,):
        lessonNumber = 0
        for week, timeTuple in self.lessonPeriod.items():
            # timeTuple[0]是上课时间，timeTuple[1]是下课时间
            lessonNumber +=self.todayLessonNumber(timeTuple[0], timeTuple[1])
        logging.info("本周总共上课节数为：%s"%(lessonNumber))
        return lessonNumber


    # 计算今天上课数
    def todayLessonNumber(self,schoolTime,quittingTime):
        schoolTime = datetime.strptime(schoolTime, '%H:%M')
        quittingTime = datetime.strptime(quittingTime, '%H:%M')
        durationTime = quittingTime - schoolTime
        # 每节课的时间是30分钟，即1800秒
        perLessonTime = 1800
        # 相除可以得到每天上几节课
        lessonNumber = int(durationTime.seconds / perLessonTime)
        logging.info("今天上课节数是:%s"%(lessonNumber))
        return lessonNumber
    # 计算总共要上几周
    def totalWeekNumber(self):
        # 向上取整
        weekNumber = math.ceil(self.totalLessonNumber()/self.weekLessonNumber())
        logging.info("总共要上：%s周"%(weekNumber))
        return weekNumber

    def getNextSchoolTime(self,lastSchoolTime):
        oneday = timedelta(days=1)
        nextSchoolTime = lastSchoolTime + oneday
        while "星期"+nextSchoolTime.strftime("%w") not in self.lessonPeriod:
            nextSchoolTime += oneday

        return nextSchoolTime
    # firstLessonCall 的作用是，调课时，要调的课通常不是第一节课，并且上一节课存在但没有编辑按钮（因为已经上过了）
    def clickEdit(self,currentLesson,firstLessonCall):
        # 点击编辑前要前确认上一个按钮没有完成按钮
        if currentLesson != 1 and firstLessonCall ==False:
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

    def setLessonTime(self,currentLesson,currentSchoolTime,lastSchoolTime,firstLessonCall=False):

        self.clickEdit(currentLesson,firstLessonCall)
        # 输入上课年-月-日：先清空内容再输入
        self.setSchoolTimeYearAndMonth(currentLesson, lastSchoolTime)
        # 设置上课时间
        self.setSchoolTimeHourAndMin(currentLesson, currentSchoolTime)

        # 设置下课时间
        self.setQuitTimeHourAndMin(currentLesson, currentSchoolTime + timedelta(minutes=30))
        # 点击保存
        self.clickSave(currentLesson)



    def lessonSchedule(self,currentLesson=0):
        lastSchoolTime = self.startTime
        for thisWeek in range(0,self.totalWeekNumber()):
            for week,timeTupe in self.lessonPeriod.items():
                currentSchoolTime = datetime.strptime(timeTupe[0], '%H:%M')
                for i in range(0,self.todayLessonNumber(timeTupe[0],timeTupe[1])):
                    # 点击课表的修改按钮
                    currentLesson+=1
                    if currentLesson > self.totalLessonNumber():
                        logging.info("课程设置完毕")
                        return
                    self.setLessonTime(currentLesson,currentSchoolTime,lastSchoolTime)
                    # 每节课为30分钟
                    currentSchoolTime += timedelta(minutes=30)
                lastSchoolTime = self.getNextSchoolTime(lastSchoolTime)

    # changedLesson以字典形式给出，{'课程':'19','日期':'2019-10-9','时间':('5:00','8:00')}，表示把第19节课更改到2019-10-9，5:00开始上课
    def setFirstLesson(self, changedLesson):
        currentLesson = int(changedLesson['课程'])
        lastSchoolTime = datetime.strptime(changedLesson['日期'], '%Y-%m-%d')
        currentSchoolTime = datetime.strptime(changedLesson['时间'][0], '%H:%M')
        for i in range(0, self.todayLessonNumber(changedLesson['时间'][0], changedLesson['时间'][1])):
            if currentLesson > self.totalLessonNumber():
                logging.info("课程设置完毕")
                return
            # True发生在第一次调课
            self.setLessonTime(currentLesson,currentSchoolTime,lastSchoolTime,True)
            currentLesson += 1
            currentSchoolTime += timedelta(minutes=30)

        return self.getNextSchoolTime(lastSchoolTime),currentLesson-1

    def adjustmentLesson(self, changedLesson):
        self.setStartTime(changedLesson['日期'])
        nextTimeAndCurrentLesson = self.setFirstLesson(changedLesson)
        self.startTime = nextTimeAndCurrentLesson[0]
        currentLesson = nextTimeAndCurrentLesson[1]
        self.lessonSchedule(currentLesson)









