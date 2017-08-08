
import logging
import logging.config
from shutil import copyfile
import time
from datetime import datetime
import re
from workerUtilities import writeToFile


# This script takes the formatted output of autorep -J ALL -n and copies the statuses using the status attribute
# the first 3 lines from the autorep output need to be deleted from the file before running the script.
# What statuses to consider to set are in the pickJobStatus List


jobNameList=[]
jobNameStatusDict = {}
jobStatusList=['IN','SU','OI','OH','IN/NE','ST','RU','TE','FA']
pickJobStatus=['SU','OI','OH','FA','TE','IN/NE']
jobStatusDictMap={'OI':'ON_ICE','OH':"ON_HOLD",'TE':'TERMINATED','IN/NE':'NO_EXEC','SU':'SUCCESS','FA':'FAILURE'}



def readJilFile(jobStatusFile):
    logging.config.fileConfig("logging.conf")
    logger=logging.getLogger("AutoSysUtils.readJilFile")
    logger.info("Testing message")
    with open(jobStatusFile) as myJilInput:
        for line in myJilInput:
            jobName=""
            jobStatus=""
            currentLine=line.strip()
            #logger.debug("Reading line: {0}".format(currentLine))
            currentLineTuple=currentLine.split()
            #logger.debug(currentLineTuple)
            jobName=currentLineTuple[0].strip()
            #logger.debug("Job Identified: {0}".format(jobName))
            if(currentLineTuple[3].strip() in jobStatusList):

                jobStatus=currentLineTuple[3].strip()

            else:
                if(currentLineTuple[4].strip() in jobStatusList):
                    jobStatus=currentLineTuple[4].strip()
                else:
                    if (currentLineTuple[5].strip() in jobStatusList):
                        jobStatus=currentLineTuple[5].strip()
            logger.debug("Job: {0} - Job Status: {1}".format(jobName, jobStatus))
            logger.debug("Adding to dictionary")
            jobNameStatusDict[jobName]=jobStatus
    print(jobNameStatusDict)


def getJobStatusFromMap(jobName):
    logger=logging.getLogger("AutoSysUtils.getJobStatusFromMap")
    logger.info("Getting Job Status for {0}".format(jobName))
    currentJobStatus=jobNameStatusDict[jobName.strip()]
    logger.debug("Job Status is: {0}".format(currentJobStatus))
    jobStatusReturn=""
    if currentJobStatus in jobStatusDictMap.keys():

        jobStatusReturn=jobStatusDictMap[currentJobStatus]
    return jobStatusReturn

def writeUpdatedJobStatusFile(sourceJil):
    logger=logging.getLogger("AutoSysUtils.writeUpdatedJobStatusFile")
    print(sourceJil)
    targetJil=sourceJil+".target"
    copyfile(sourceJil,sourceJil+".orig")
    #copyfile(sourceJil,targetJil)
    with open(sourceJil) as myJil:
        for line in myJil:
            currentJilLine=line.strip()
            writeToFile(targetJil, line)
            if(re.match("insert_job",currentJilLine,flags=0)):
                jobTuple=currentJilLine.split()
                #print(jobTuple)
                logger.info("Job Name found: {0}".format(jobTuple[1]))
                jobNameList.append(jobTuple[1])
                statusAttrib = addAttribute("status", getJobStatusFromMap(jobTuple[1]))
                logger.debug("Length of Status attribute {0} is {1}".format(statusAttrib,len(statusAttrib)))
                if(len(statusAttrib)>8):
                    writeToFile(targetJil,statusAttrib)





def addAttribute(attrName,attrValue):
    print(attrName,":",attrValue)
    statusAttribute=attrName+":"+attrValue
    return statusAttribute+"\n"
