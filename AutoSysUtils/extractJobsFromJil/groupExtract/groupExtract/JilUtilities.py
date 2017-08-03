import re
import logging
import logging.config
import collections
from collections import defaultdict

jobList=[]
jobsetList=[]
jobsetJobMap=defaultdict(list)
ignoreLineList=['/*','#  ----------------- DIAGNOSTIC:','#  -----------------','CONVERSION']
machineList=[]
resourceList={}
jobCommandMap={}
jobConditionMap={}

def writeToFile(outputFile, line):
    fileWriter = open(outputFile,"a")
    fileWriter.write(line+"\n")


def readJilForCommandAndCondition(jilInputFile):
    logger=logging.getLogger("JPMC-JilAnalyzer.readJilForCommandAndCondition")
    logger.info("Reading {0} to extract jobname, command and condition attribute ".format(jilInputFile))
    with open(jilInputFile) as myJil:
        for line in myJil:
            currentJilLine=line.strip()
            if("insert_job" in currentJilLine):
                logger.debug(currentJilLine)
                jobName=currentJilLine.partition("insert_job:")[2].partition("job_type:")[0].strip()
                jobType=currentJilLine.partition("job_type:")[2].strip()
            if("command" in currentJilLine):
                jobCommand=currentJilLine.partition("command:")[2].strip()
            if("condition:" in currentJilLine):
                jobCondition=currentJilLine.partition("condition")[2].strip()
            if(not jobName is None):
                jobConditionMap[jobName]=jobCondition
                jobCommandMap[jobName]=jobCommand

def readJil(inputJilFile,resOutFile,machineOutFile):
    logger=logging.getLogger("AutoSysUtilities.JilUtilities.readJil")
    jobName=""
    jobType=""
    job_owner=""
    box_name=""
    resourceName=""
    resourceType=""
    resourceAmt=""
    run_machine=""
    with open(inputJilFile) as myJil:
        for line in myJil:
            currentJilLine=line.strip()
            if(currentJilLine in ignoreLineList):
                logger.debug("Ignoring current line: {0} ".format(currentJilLine))
            else:
                if("insert_job" in currentJilLine):
                    logger.info("Job Definition line found. Checking job type")
                    jobName=currentJilLine.partition("insert_job:")[2].partition("job_type:")[0].strip()
                    if("job_type:" in currentJilLine):
                        jobType=currentJilLine.partition("job_type:")[2].strip()
                    if(not jobName in jobList):
                        jobString=jobName+"-"+jobType
                        jobList.append(jobString)
                if("machine: " in currentJilLine):
                    run_machine=currentJilLine.partition("machine:")[2].strip()
                    if(not run_machine in machineList):
                        machineList.append(run_machine)
                if("owner:" in currentJilLine):
                    job_owner=currentJilLine.partition("owner:")[2].strip()
                if("box_name:" in currentJilLine):
                    box_name=currentJilLine.partition("box_name")[2].strip()
                if("resources:" in currentJilLine):
                    tempresourceName=currentJilLine.partition("resources:")[2].strip()
                    resourceTuple=tempresourceName.split(',')
                    resourceName=resourceTuple[0].replace('(','').strip()
                    resourceAmt=resourceTuple[1].partition("QUANTITY")[2].replace('=','').strip()
                    #resourceType=resourceTuple[2].replace(')','').strip()
                    keyList=resourceList.keys()
                    if(not resourceName in list(resourceList.keys())):
                        resourceList[resourceName]=resourceAmt
    logger.info("Done searching for jobs, machines and resources.")
    logger.info("Total Number of jobs: {0}".format(len(jobList)))
    logger.info("Total Number of machines: {0}".format(len(machineList)))
    logger.info("Total number of resources: {0}".format(len(resourceList)))
    for resource in resourceList:
        writeToFile(resOutFile,"insert_resource: "+resource)
        writeToFile(resOutFile,"res_type: R")
        writeToFile(resOutFile,"amount: "+resourceAmt)
        writeToFile(resOutFile,"\n")
    for machine in machineList:
        writeToFile(machineOutFile,"insert_machine: "+machine)
        writeToFile(machineOutFile,"\n")

