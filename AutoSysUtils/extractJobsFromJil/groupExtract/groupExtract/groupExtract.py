import re
import logging
import logging.config
from datetime import datetime
import time
import os
import collections
from collections import defaultdict
import xlrd
import JilUtilities
from JilUtilities import readJil
from workerUtilities import writeToFile



topBoxList=[]
topBoxTime=[]
fileTriggerList=[]
fileTriggerMap={}
fileTriggerCalendarMap=defaultdict(list)


jobsetsInTopBox=defaultdict(list)  # Contains a collection of the following format:
# {topbox: box1,box2}



def readExcelForTopLevel(topLevelFile,sheetName):
    logger = logging.getLogger("JMO_AE_Utils.groupExtract.readExcelForTopLevel")
    logging.info("Reading top level file...")
    #Oopening Workbook
    workbook = xlrd.open_workbook(topLevelFile)
    #Oopen sheet by name
    workSheet = workbook.sheet_by_name(sheetName)
    rowCount=workSheet.nrows
    colCount=workSheet.ncols
    topBoxName=""
    topBoxTime=""
    topBoxCalendar=""
    topBoxJobsetName=[]
    topboxJobset=""

    logger.info("Total number of rows is: {0} and total number of columns is: {1}".format(rowCount,colCount))
    for rowNum in range(1,rowCount):
        for colNum in range(0,4): # Reading only the first 4 columns. if we have to read all columns, then replace with the colCount variable.
            logger.info("Reading cell {0},{1}".format(rowNum,colNum))
            cellData=workSheet.cell(rowNum,colNum).value.strip()
            logger.info(type(colNum))
            if(colNum==0):
                logger.info("Reading top box name")
                topBoxName=workSheet.cell(rowNum,colNum).value.strip()
                if(not topBoxName in topBoxList):
                    topBoxList.append(topBoxName)
            if(colNum==1):
                logger.info("Reading top box start time")
                topBoxTimes=workSheet.cell(rowNum,colNum).value.strip()
                #topBoxWithTime=topBoxName+":"+topBoxTimes
                
            if(colNum==2):
                
                logger.info("Reading top box calendar")
                topBoxCalendar=workSheet.cell(rowNum,colNum).value.strip()
                #topBoxWithTime_Cal=topBoxWithTime+":"+topBoxCalendar
               
            if(colNum==3):
                logger.info("Reading jobset to be part of top box")
                topboxJobset=workSheet.cell(rowNum,colNum).value.strip()
                jobsetWithTime_Cal=topboxJobset+"-"+topBoxTimes+"-"+topBoxCalendar
                if(not topboxJobset in topBoxJobsetName):
                    topBoxJobsetName.append(topboxJobset)
                    jobsetsInTopBox[topBoxName.strip()].append(jobsetWithTime_Cal)
                else:
                    logger.info("Top box jobset: {0} already exists. Not adding")
                    valueList=jobsetsInTopBox[topBoxName.strip()]
                    if(not jobsetWithTime_Cal in valueList):

                        jobsetsInTopBox[topBoxName.strip()].append(jobsetWithTime_Cal)
                    else:
                        logger.info(jobsetWithTime_Cal + " already exists as a Value.")
                    
            
            logger.debug("Cell Data at {0},{1} is {2}".format(rowNum,colNum,cellData))
            print(jobsetsInTopBox)
            writeToFile("C:\\JMOFiles\\TopLevelBoxes_Jobsets.txt")
            

def getConditionsForJob(jobName):
    logger=logging.getLogger("JMO_AE_Utils.groupExtract.getConditionsForJob")
    logger.info("Getting conditions for job: {0} ".format(jobName))
    logger.info("Establishing database connection...")

def readJilForFileWatchers(jilFileName,convertJobNames):
    logger=logging.getLogger("JMO_AE_Utils.groupExtract.readJilForFileWatchers")
    ftjobName=""
    ftWatchFile=""
    ftCalendar=""
    ftDaysOfWeek=""
    ftStartTimes=""
    ftStartMins=""
    jobFound=False
    logger.info("Reading {0} to get all File Triggers and Filewatchers".format(jilFileName))
    with open(jilFileName) as myFTJil:
        for line in myFTJil:
            currentLine=line.strip()
            if(("insert_job:" in currentLine and "job_type: FT" in currentLine) or ("insert_job:" in currentLine and "job_type: FW" in currentLine)):
                jobFound=True
                logger.info("Found FT/FW job")
                logger.debug(currentLine)
                ftjobName=currentLine.partition("insert_job:")[2].partition("job_type:")[0].strip()
                logger.info("FT/FW job name: {0}".format(ftjobName))

            if(("watch_file:" in currentLine and jobFound==True and (not "#" in currentLine))):

                logger.info("watch_file attribute found")
                ftWatchFile=currentLine.partition("watch_file:")[2].strip()
            if("run_calendar:" in currentLine and jobFound==True and (not "#" in currentLine)):
                logger.info("Run calendar associated with FT/FW job")
                ftCalendar=currentLine.partition("run_calendar:")[2].strip()
               
            if("days_of_week:" in currentLine and jobFound==True and (not "#" in currentLine)):
                logger.info("days_of_week attribute associated with FW/FT job")
                ftDaysOfWeek=currentLine.partition("days_of_week:")[2].strip()

            if("start_times:" in currentLine and jobFound==True and (not "#" in currentLine)):
                logger.info("start_times attribute associated with FW/FT job")
                ftStartTimes=currentLine.partition("start_times:")[2].strip()

            if("start_mins:" in currentLine and jobFound==True and (not "#" in currentLine)):
                logger.info("start_mins attribute associated with FW/FT job")
                ftStartMins=currentLine.partition("start_mins:")[2].strip()

            if(jobFound==True and not ftWatchFile=="" and ftjobName not in fileTriggerList):
                logger.info("Job {0} added to fileTriggerList".format(ftjobName))
                fileTriggerList.append(ftjobName)
                fileTriggerMap[ftjobName]=ftWatchFile
            if(not ftCalendar=="" and ftDaysOfWeek=="" ):
                calendarJobList=[]
                calendarJobList=fileTriggerCalendarMap[ftCalendar]
                if(not ftjobName in calendarJobList):
                    logger.info("Adding job {0} to calendar: {1}".format(ftjobName,ftCalendar))
                    
                    calendarJobList.append(ftjobName)
                    fileTriggerCalendarMap[ftCalendar]=calendarJobList
            if(ftCalendar=="" and not ftDaysOfWeek==""):
                calendarJobList=[]
                calendarJobList=fileTriggerCalendarMap[ftDaysOfWeek]
                calendarJobList.append(ftjobName)
                fileTriggerCalendarMap[ftCalendar]=calendarJobList
    
    if(convertJobNames=="0"):
        logger.info("Not converting job names to have the extension from the watch_file attribute at the end")
        logger.info("Setting FT in Top level boxes per calendar")

    if(convertJobNames=="1"):
        logger.info("Converting job names to have the extension from the watch_file attribute at the end")
        logger.info("Setting FT in Top level boxes per calendar")


def readJilForGroup(jilInputFile,groupSearchString,topBoxName,topBoxCalendar,topBoxTime):
    jobName=""
    currentTime=time.strftime("%Y%m%d-%HH%M%S")
    logger = logging.getLogger("JMO_AE_Utils.groupExtract.readJilForGroup")
    # This file creates the jil to move the boxes into the Top Box.
    with open(jilInputFile) as jilInput:
        for line in jilInput:
            currentJilLine=line.strip()
            if("insert_job" in currentJilLine):
                logger.debug("Job Line found")
                jobName=currentJilLine.partition("insert_job:")[2].partition("job_type:")[0].strip()
                jobType=currentJilLine.partition("job_type:")[2].strip()
            groupAttribute="group: "+groupSearchString
            applAttribute="application: "+groupSearchString
            if(((groupSearchString in currentJilLine)  and (not "#" in currentJilLine)) and jobType=="BOX"):
                logger.info("Match found: {0} with search string: {1} ".format(jobName,groupSearchString))
                logger.debug("Current Line: {0}".format(currentJilLine))
                print("update_job: "+jobName)
                print("box_name: "+topBoxName)
                print("date_conditions: 0")
                #print("start_times: "+topBoxTime)
                writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBox_"+topBoxName+"-"+currentTime+".jil","update_job: "+jobName)
                writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBox_"+topBoxName+"-"+currentTime+".jil","box_name: "+topBoxName) 
                writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBox_"+topBoxName+"-"+currentTime+".jil","date_conditions: 0")
                #writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","start_times: "+topBoxTime)
                #writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","run_calendar: "+topBoxCalendar)
                writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBox_"+topBoxName+"-"+currentTime+".jil","\n")


