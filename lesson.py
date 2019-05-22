
from datetime import datetime
from datetime import timedelta
import logging
import math
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
        self.startTime = datetime.strptime(startTime, '%Y-%m-%d')
        openCalendar = self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[1]/div[1]/div/div[1]/i')
        openCalendar.click()
        currentTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[2]').text
        startTimeFormated = '%s年%s月'%(self.startTime.year,self.startTime.month)
        while  currentTime != startTimeFormated:
            currentTimeFormated = datetime.strptime(currentTime, '%Y年%m月')
            if currentTimeFormated < self.startTime:
                nextMonth =  self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[3]')
                nextMonth.click()
            elif currentTimeFormated > self.startTime:
                lastMonth = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[1]')
                lastMonth.click()
            currentTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[2]').text
        findStartTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/tbody//td[@data-date="%s/%s/%s"]'%(self.startTime.year,self.startTime.month,self.startTime.day))
        findStartTime.click()

    # lessonPeriod 以字典形式给出，{'星期几':'上课时间',...},0代表星期日，6代表星期6。比如{'星期5':('14:00','15:00'),'星期0':('15:00','18:00')}
    def setWeekArrangement(self,lessonPeriod):
        self.lessonPeriod = lessonPeriod

    # 设置一周上几节课
    def weekLessonNumber(self):
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

    def 



    def lessonSchedule(self):
        currentLesson = 0
        lastSchoolTime = self.startTime
        for thisWeek in range(0,self.totalWeekNumber()):
            for week,timeTupe in self.lessonPeriod.items():
                lastSchoolTime = self.getNextSchoolTime(lastSchoolTime)
                currentSchoolTime = datetime.strptime(timeTupe[0], '%H:%M')
                quittingTime = datetime.strptime(timeTupe[1], '%H:%M')

                for i in range(0,self.todayLessonNumber(timeTupe[0],timeTupe[1])):
                    # 点击课表的修改按钮
                    currentLesson+=1
                    if currentLesson > self.totalLessonNumber():
                        logging.info("课程设置完毕")
                        return

                    js4= 'var q= document.querySelector("#livetime_increase_0 > div.guide-bd.form.form--h > div.f-item.f-item-livetask > div > ul > li:nth-child(%s) > div.ct-show > a").click()'%(currentLesson)
                    self.driver.execute_script(js4)
                    # 输入上课年-月-日：先清空内容再输入
                    self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[1]/input'%(currentLesson)).clear()
                    logging.info("currentLesson = "+str(currentLesson))
                    self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[1]/input'%(currentLesson)).send_keys( lastSchoolTime.strftime("%Y-%m-%d"))
                    # 设置上课时间
                    self.driver.find_element_by_xpath(
                        '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[1]/div[1]/input' % (
                            currentLesson)).clear()
                    self.driver.find_element_by_xpath(
                        '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[1]/div[1]/input'%(
                            currentLesson)).send_keys(currentSchoolTime.strftime("%H:%M"))
                    currentSchoolTime += timedelta(minutes=30)
                    # 设置下课时间
                    logging.info("下课时间："+currentSchoolTime.strftime("%H:%M"))
                    self.driver.find_element_by_xpath(
                        '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[2]/div[1]/input' % (
                            currentLesson)).clear()
                    self.driver.find_element_by_xpath(
                        '//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[2]/div[2]/div[1]/input' % (
                            currentLesson)).send_keys(currentSchoolTime.strftime("%H:%M"))
                    #点击保存
                    self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/a[1]'%(currentLesson)).click()















