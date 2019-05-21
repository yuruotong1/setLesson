import time
import datetime
import logging
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
        self.startTime = time.strptime(startTime, '%Y-%m-%d')
        openCalendar = self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[1]/div[1]/div/div[1]/i')
        openCalendar.click()
        currentTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[2]').text
        startTimeFormated = '%s年%s月'%(self.startTime.tm_year,self.startTime.tm_mon)
        while  currentTime != startTimeFormated:
            currentTimeFormated = time.strptime(currentTime, '%Y年%m月')
            if currentTimeFormated < self.startTime:
                nextMonth =  self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[3]')
                nextMonth.click()
            elif currentTimeFormated > self.startTime:
                lastMonth = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[1]')
                lastMonth.click()
            currentTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/thead/tr[1]/th[2]').text
        findStartTime = self.driver.find_element_by_xpath('/html/body/div[7]/div/table/tbody//td[@data-date="%s/%s/%s"]'%(self.startTime.tm_year,self.startTime.tm_mon,self.startTime.tm_mday))
        findStartTime.click()

    # weekAndTime 以字典形式给出，{'星期几':'上课时间',...}。比如{'星期五':('14:00','15:00'),'星期六':('15:00','18:00')}
    def setWeekArrangement(self,weekAndTime):
        self.weekAndTime = weekAndTime

    # 设置一周上几节课
    def weekLessonNumber(self):
        lessonNumber = 0
        for week, timeTuple in self.weekAndTime.items():
            # timeTuple[0]是上课时间，timeTuple[1]是下课时间
            lessonNumber +=self.todayLessonNumber(timeTuple[0], timeTuple[1])
        logging.info("本周总共上课节数为：%s"%(lessonNumber))
        return lessonNumber


    # 计算今天上课数
    def todayLessonNumber(self,schoolTime,quittingTime):
        schoolTime = datetime.datetime.strptime(schoolTime, '%H:%M')
        quittingTime = datetime.datetime.strptime(quittingTime, '%H:%M')
        durationTime = quittingTime - schoolTime
        # 每节课的时间是30分钟，即1800秒
        perLessonTime = 1800
        # 相除可以得到每天上几节课
        lessonNumber = int(durationTime.seconds / perLessonTime)
        logging.info("今天上课节数是:%s"%(lessonNumber))
        return lessonNumber
    # 计算总共要上几周
    def totalWeekNumber(self):
        lessonNumber = self.totalLessonNumber()/self.weekLessonNumber()
        logging.info("总共要上：%s周"%(lessonNumber))
        return lessonNumber

    def lessonSchedule(self):
        totalLessons = self.totalLessonNumber()
        #todo: 先计算出startTime 是第几周，然后计算需要几周，下面range的起始不是1
        for thisWeek in range(1,self.totalWeekNumber()):
            for week,timeTupe in self.weekAndTime:
                #todo：要根据哪年，第几周，星期几计算出年-月-日
                weekFormated = datetime.datetime.strptime(week, '星期%w')

                todayCalFormated = datetime.datetime.strptime(thisWeek+week,'')
                for i in range(0,self.todayLessonNumber(timeTupe[0],timeTupe[1])):
                    #todo：计算出课程号的排序算法
                    pass


        # 点击课表的修改按钮
            js4= 'var q=document.querySelector("#livetime_increase_0 > div.guide-bd.form.form--h > div.f-item.f-item-livetask > div > ul > li:nth-child(%s) > div.ct-edit > div > div.f-dates > i").click()'%(number)
            self.driver.execute_script(js4)
        # 输入上课时间：先清空内容再输入
        # 查看第几周，星期几对应的日期
            print(time.strptime('2019-1-1', '%Y-%U-%w').tm_mon)
            self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[1]/input'%(thisWeek)).clear()
            self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul/li[%s]/div[2]/div/div[1]/input'%(thisWeek)).send_keys("2019-8-14")













