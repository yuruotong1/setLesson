import time
import datetime
import logging
class Lesson:
    def __init__(self,driver):
        self.driver = driver


    def number(self):
        ul = self.driver.find_element_by_xpath('//*[@id="livetime_increase_0"]/div[2]/div[2]/div/ul')
        lis = ul.find_elements_by_xpath('li')
        return len(lis)
    # setStartTIme设置直播开始日期，格式：年-月-日。比如2019-5-19
    def setStartTime(self,startTime):
        self.startTime = time.strptime(startTime, '%Y-%m-%d')

    # weekAndTime 以字典形式给出，{'星期几':'上课时间',...}。比如{'星期五':('14:00','15:00'),'星期六':('15:00','18:00')}
    def weekArrangement(self,weekAndTime):
        for week,timeTuple in weekAndTime.items():
            # timeTuple[0]是上课时间，timeTuple[1]是下课时间
            self.todayLessonNumber(timeTuple[0],timeTuple[1])



    def todayLessonNumber(self,schoolTime,quittingTime):
        schoolTime = datetime.datetime.strptime(schoolTime, '%H:%M')
        quittingTime = datetime.datetime.strptime(quittingTime, '%H:%M')
        durationTime = quittingTime - schoolTime
        # 每节课的时间是30分钟，即1800秒
        perLessonTime = 1800
        # 相除可以得到每天上几节课
        lessonNumber = int(durationTime.seconds / perLessonTime)
        logging.info("上课节数是:%s"%(lessonNumber))
        return lessonNumber
    def lessonSchedule(self):
        self.startTime






