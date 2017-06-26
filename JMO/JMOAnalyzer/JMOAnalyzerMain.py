import re
import logging
import logging.config
from datetime import datetime
import time
import os
import collections
from collections import defaultdict

baseConversionFolder = "D:\\JPMC-JMO\\JMO2AE-Conversion"
jmoReportFile = "D:\JPMC-JMO\Reports\JMOReport.txt"

jobDefString = "DEFINE JOB ID="
jobsetDefString = "DEFINE JOBSET ID="
jobpredDefString = "DEFINE JOBPRED ID="
jobsetpredDefString = "DEFINE JOBSETPRED ID="
stationDefString = "DEFINE STATION ID="
triggerDefString = "DEFINE TRIGGER ID="
resourceDefString = "DEFINE RESOURCE ID="
jobresDefString = "DEFINE JOBRES ID="
jobsetresDefString = "DEFINE JOBSETRES ID="
stationgroupDefString = "DEFINE STATIONGROUP ID="
calendarDefString = "DEFINE CALENDAR ID="
jobparmDefString = "DEFINE JOBPARM ID="
critKeyString = "CRITKEYS="
critcalString = "CRITCAL="
critHolidayActionString = "CRITHACT="

jobInT2=False
jobsetInT2=False
jobInT4=False
jobsetInT4=False


unqstationList = []
unqjobList = []
unqjobSetList = []
unqcalendarList = []
unqresourceList = []
unqtriggerList = []
jobStationMap = []  # Contains a mapping between jobs and stations. What jobs run on what stations.
jobsetStationMap = []  # Contains a mapping between jobsets and stations.
jobJobsetMap = defaultdict(
    list)  # Dictionary of keys=jobsets and jobs=jobset,job,jobnumber. This is similiar to Dictionary(String, List<String>) in c# or Java
jmoJobList = []  # List of all jobs. Will contain non-unique jobs
jobmultiple = 0
triggerMultiple = 0

jmoExtractFile = "";


def main():
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("JPMC-JMO-Analyzer.main")
    jmoExtractFile = input("Enter the full path to the JMO Extract: ")
    logger.info("Reading {0} ")
    readJMOExtract(jmoExtractFile)


def getObjectsFromString(jobString, type):
    global jobmultiple
    logger = logging.getLogger("JPMC-JMO-Analyzer.getJobNameString")

    # tempString=jobString.replace('(','')
    # tempString1=tempString.replace(')','')
    # logger.debug(tempString1)
    myTempString = ""
    if ("CRITKEYS" in jobString):
        myTempString = jobString.partition("CRITKEYS")[0].strip()
    elif ("DESCRIPTION" in jobString and not "CRITKEYS" in jobString):
        myTempString = jobString.partition("DESCRIPTION")[0].strip()
    elif ("PRIORITY" in jobString):
        myTempString = jobString.partition("PRIORITY")[0].strip()
    elif ("STATION" in jobString):
        myTempString = jobString.partition("STATION")[0].strip()
    else:
        logger.debug(jobString)
    if (type == "JOB"):
        if (len(myTempString) > 0):
            tempString1 = myTempString
        else:
            tempString1 = jobString
            logger.debug(tempString1)

        logger.debug("Parsing {0} for jobset, job and job number".format(tempString1))
        stringTuple = tempString1.split(',')
        jobsetName = stringTuple[0].strip()
        jobName = stringTuple[1].strip()
        jobNumber = stringTuple[2].replace(")", "").strip()
        jobNameJobNumber = jobName + "," + jobNumber
        logger.debug("Added {0} to the dictionary".format(jobNameJobNumber))
        jobJobsetMap[jobsetName.strip()].append(jobNameJobNumber)
        # if(not jobsetName  in jobJobsetMap.keys()):
        # jobJobsetMap[jobsetName.strip()]=jobNameJobNumber.strip()
        # else:
        # get values for the current jobset in a list
        # print(jobJobsetMap)
        # jobList=jobJobsetMap[jobsetName.strip()]
        # logger.debug(jobList)
        # logger.debug(type(jobList))
        # jobList.append(jobNameJobNumber.strip())
        # jobJobsetMap.update({jobsetName.strip():jobList})
        print(jobJobsetMap)
        if (jobNameJobNumber in unqjobList):
            logger.debug("Job {0} and Job Number {1} already exist. Making unique".format(jobName, jobNumber))
            jobmultiple = jobmultiple + 1
            multiNumberString = ".m" + str(jobmultiple)
            newJobNameString = jobName + multiNumberString + jobNumber  # Provides the m1, m2 functionality on jobs.
            unqjobList.append(newJobNameString)
            logger.debug("{0} added to jmoJobList".format(newJobNameString))

        if (not jobNameJobNumber in unqjobList):
            unqjobList.append(jobNameJobNumber)
            logger.debug("{0} added to jmoJobList".format(jobNameJobNumber))


def readJMOExtract(jmoExtract):
    logger = logging.getLogger("JPMC-JMO-Analyzer.readJMOExtract")
    myTime = time.strftime("%c")
    logger.info("Parsing {0} for analysis. Started at {1}".format(jmoExtract, myTime))
    # Check for Jobs and add jobs to job list
    # Check for JObsets and add jobsets to jobset list
    # Check for Triggers and add to trigger List
    # Check for stations and add to Stations list
    # Check for Resources and add to Resources List
    # Check for job predecessors and add to job predecessor list
    # Check for jobset predecessors and add to jobset predecessor list
    # Check for Calendars and add to Calendar List

    with open(jmoExtract) as myJMOExtract:
        for line in myJMOExtract:
            currentLine = line.strip()

            if (re.match(jobDefString, currentLine, flags=0)):
                logger.debug("Job Definition found...")
                logger.debug(currentLine)
                tempJobString = currentLine.partition(jobDefString)[2].partition("FAILCOND")[0].strip()
                logger.debug("Job Name: {0}".format(tempJobString))
                getObjectsFromString(tempJobString, "JOB")
            if (re.match(jobsetDefString, currentLine, flags=0)):
                logger.debug("Jobset Definition found...")
                logger.debug(currentLine)
                tempJobsetString = currentLine.partition(jobsetDefString)[2].partition("FAILCOND")[0].strip()
                logger.debug("Jobset Name: {0}".format(tempJobsetString))
                if (not tempJobsetString in unqjobSetList):
                    unqjobSetList.append(tempJobsetString)
            if (re.match(stationDefString, currentLine, flags=0)):
                logger.info("Station definition found")
                # logger.debug(currentLine)
                myStationString = currentLine.partition(stationDefString)[2].partition("NODE")[0].strip()
                myStationTuple = myStationString.split(',')
                stationName = myStationTuple[0].replace('(', "").strip()
                stationType = myStationTuple[1].replace(')', "").strip()
                if (not stationName in unqstationList):
                    unqstationList.append(stationName)
            if (re.match(triggerDefString, currentLine, flags=0)):
                global triggerMultiple
                logger.info("Trigger Definition found")
                logger.debug(currentLine)
                tempTriggerID = currentLine.partition(triggerDefString)[2].partition("DESCRIPTION=")[0].strip()
                myTriggerSplits = tempTriggerID.split(',')
                # logger.debug(myTriggerSplits)
                myTriggerID = myTriggerSplits[0].strip().replace('(', "")
                myTriggerType = myTriggerSplits[1].replace(')', "").strip()
                logger.debug("Adding Trigger: {0} to triggerList".format(myTriggerID))
                # if(not myTriggerID in unqtriggerList):
                # unqtriggerList.append(myTriggerID)
                # if(myTriggerID in unqtriggerList):
                # logger.debug("Trigger {0} already exist. Making unique".format(myTriggerID))
                # triggerMultiple=triggerMultiple+1
                # multiNumberString=".m"+str(triggerMultiple)
                # newJobNameString=myTriggerID+multiNumberString # Provides the m1, m2 functionality on triggers.
                # unqtriggerList.append(newJobNameString)
                unqtriggerList.append(myTriggerID)
            if (re.match(resourceDefString, currentLine, flags=0)):
                logger.info("Resource definition found")
                # logger.debug(currentLine)
                tResourceLine = currentLine.partition(resourceDefString)[2].partition("DESCRIPTION")[0].strip()
                resDef = tResourceLine.split(',')
                resName = resDef[0].replace('(', "")
                resType = resDef[1].replace(')', "")
                resAmount = currentLine.partition("AMOUNT")[2].partition("WEIGHT")[0].strip()
                if (not resName in unqresourceList):
                    # jmoResourceList.append(resName+":"+resType+":"+resAmount)
                    logger.debug("{0} added to jmoResourceList".format(resName + ":" + resType + ":" + resAmount))
                    unqresourceList.append(resName + ":" + resType + ":" + resAmount)
            if (re.match(jobpredDefString, currentLine, flags=0)):
                logger.info("Job Predecessor found. Parsing...")
                if ("PJNO" in currentLine and "PSET" in currentLine):
                    logger.debug("Job has other job predecessors. Not just jobset.")
                    currentJobString = currentLine.partition(jobpredDefString)[2].partition("PJOB")[0].strip()
                    predecessorJobString = currentLine.partition("PJOB=")[2].partition("PSET")[0].strip()
                    predecessorJobsetString = currentLine.partition("PSET=")[2].partition("PJNO")[0].strip()
                    predecessorJobNumberString=currentJobString.partition("PJNO=")[2].partition("WORKDAY")
                    logger.debug("Current Job Info: {0}".format((currentJobString)))
                    logger.debug("Dependent Job Info: {0}".format(predecessorJobString))
                    logger.debug("Dependent Jobset Info: {0}".format(predecessorJobsetString))
                    if("WORKDAY" in currentLine):
                        predecessorJobNumberString = currentLine.partition("PJNO=")[2].partition("WORKDAY")[0].strip()
                    if("WORKDAY" in currentLine and "TRID" in currentLine):
                        logger.debug("Job depends on trigger")
                        currentJobString = currentLine.partition(jobpredDefString)[2].partition("WORKDAY")[0].strip()
                        triggerName=currentLine.partition("TRID=")[2].strip()
                        triggerType=currentLine.partition("TREV")[2].partition("TRID")[0].strip()
                else:
                    if (not "PJNO" in currentLine):
                        logger.debug("Job depends only on other jobset.")

    print(jobJobsetMap)
    createFinalJMOReport()


def getDuplicateTriggers():
    logger = logging.getLogger("JPMC-JMO-Analyzer.getDuplicateTriggers")
    print(set([x for x in unqtriggerList if unqtriggerList.count(x) > 1]))

def checkIfPredExists():
    logger=logging.getLogger("JPMC-JMO-Analyzer.predecessorCheck")
    tranche4File="D:\OneDrive-Business\OneDrive - Robert Mark Technologies\JPMC-JMO-Conversion\JMO_Extracts\combinedextracts\P4-Extract.txt"


def checkIfPredExistsInT2():
    logger = logging.getLogger("JPMC-JMO-Analyzer.predecessorCheck")
    tranche2File="D:\OneDrive-Business\OneDrive - Robert Mark Technologies\JPMC-JMO-Conversion\JMO_Extracts\combinedextracts\P2-Extract.txt"


def writeToFile(outFile, myLine, mode):
    fileWriter = open(outFile, mode)
    fileWriter.write(myLine + "\n")
    fileWriter.close()


def createFinalJMOReport():
    getDuplicateTriggers()
    for job in unqjobList:
        writeToFile("D:\JPMC-JMO\Reports\T4_Jobs.txt", job, "a")
    for jobset in unqjobSetList:
        writeToFile("D:\JPMC-JMO\Reports\T4_Jobsets.txt", jobset, "a")
    for jobset in jobJobsetMap.keys():
        writeToFile("D:\JPMC-JMO\Reports\T4_JobMap.txt", jobset, "a")
        for item in jobJobsetMap:
            job = jobJobsetMap[jobset]
            for myjob in job:
                writeToFile("D:\JPMC-JMO\Reports\T4_JobMap.txt", "  " + myjob, "a")
            writeToFile("D:\JPMC-JMO\Reports\T4_JobMap.txt", "  " + "\n", "a")
    myTime = time.strftime("%c")
    writeToFile(jmoReportFile, "JMO Report Start @ {0} ".format(myTime), "a")

    writeToFile(jmoReportFile, "Total number of Stations in file {0}".format(len(unqstationList)), "a")
    writeToFile(jmoReportFile, "Total number of Jobs in file: {0}".format(len(unqjobList)), "a")
    writeToFile(jmoReportFile, "Total number of Jobsets in file: {0}".format(len(unqjobSetList)), "a")
    writeToFile(jmoReportFile, "Total number of Resource Definitions in file: {0}".format(len(unqresourceList)), "a")
    # writeToFile(jmoReportFile, "Total Jobset Predecessors: {0}".format(len(jobsetPredMap)))
    # writeToFile(jmoReportFile, "Total Job Predecessors: {0}".format(len(jobPredMap)))
    # writeToFile(jmoReportFile,"Total number of calendars/critkeys used in file: {0}".format(len(jmoCalendarList)))


main()
