# This module extracts the jil definition from a jil file
import re
import logging
import logging.config
import os
from datetime import datetime

from boto.glacier import job

outputFolder="D:\\JilExtracts"
CustomerName="Goldman-Sachs"



def writeToFile(inputString,outputFile):
    fileWriter = open(outputFile, "a")
    fileWriter.write(inputString)

def readJobNamesList(inputFile, jobList,outputFile):
    jobFound = False
    jobFound2 = False
    jilOutputFolder = outputFolder+CustomerName
    with open(inputFile) as myJilFile:
        for currentJilLine in myJilFile:
            if("insert_job" in currentJilLine):
                jobName = currentJilLine.partition("insert_job:")[2].partition("job_type:")[0].strip()
                if(jobName in jobList):
                    jobFound = True

                else:
                    jobFound=False

            if(jobFound==True):
                print(currentJilLine.strip())
                writeToFile(currentJilLine,outputFile)






def main():
    jobsList = []
    jobsList.append("PARA-BRAZIL_VENDOR")
    jobsList.append("SPOC-PURGE")
    readJobNamesList("D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\\Goldman\\gs_jobdef\extracts\\CNT.jil",jobsList,"D:\\extract.jil")

main()