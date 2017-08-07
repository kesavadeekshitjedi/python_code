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
#import cx_Oracle


topBoxList=[]
topBoxTime=[]


jobsetsInTopBox=defaultdict(list)  # Contains a collection of the following format:
# {topbox: box1,box2}



def readExcelForTopLevel(topLevelFile,sheetName):
    logger = logging.getLogger("JPMC-JilAnalyzer.readExcelForTopLevel")
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
            

def getConditionsForJob(jobName):
    logger=logging.getLogger("JPMC-JobAnalyzer.getConditionsForJob")
    logger.info("Getting conditions for job: {0} ".format(jobName))
    logger.info("Establishing database connection...")



def readJilForGroup(jilInputFile,groupSearchString,topBoxName,topBoxCalendar,topBoxTime):
    jobName="";
    
    logger = logging.getLogger("JPMC-JilAnalyzer.GetJobsWithGroupAttribute")
    
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
                #print("date_conditions: 1")
                #print("start_times: "+topBoxTime)
                writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","update_job: "+jobName)
                writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","box_name: "+topBoxName) 
                #writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","date_conditions: 1")
                #writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","start_times: "+topBoxTime)
                #writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","run_calendar: "+topBoxCalendar)
                writeToFile("C:\\JMOFiles\TopBox_"+topBoxName+".jil","\n")


