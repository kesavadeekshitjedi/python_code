import re
import logging
import logging.config
import collections
from collections import defaultdict

jobMapDict = defaultdict(list)
job_machine_owner_list = []

def write_to_file(inputString,outputFile):
    logger=logging.getLogger("uboc.extract_info.write_to_file")
    logger.debug(inputString)
    fileWriter = open(outputFile, "a")
    fileWriter.write(inputString)

def main():
     # Initialize logging
    logging.config.fileConfig("logging.conf")
    logger=logging.getLogger("uboc.extract_info.main")
    logger.info("Logging Initialized....")
    readJil("C:\\Users\\kesav\\OneDrive - Robert Mark Technologies\\RMT-Arch\\UnionBank\\prodjil.txt")


def readJil(jilInputFile):
    jobName=""
    jobOwner=""
    jobMachine=""
    jobFound=False

    logger = logging.getLogger("uboc.extract_info.readJil")
    logging.info("Reading {0} ".format(jilInputFile))
    with open(jilInputFile) as jilInput:
        for line in jilInput:
            currentJilLine=line.strip()
            if("insert_job" in currentJilLine):
                jobName = ""
                jobOwner = ""
                jobMachine = ""
                logger.info("Job Definition found {0}".format(currentJilLine))
                jobFound=True
                jobName=currentJilLine.partition("insert_job:")[2].partition("job_type:")[0].strip()
                #logger.debug("Job Name is "+jobName)
                if("MPCSUPRD101" in currentJilLine):
                    logger.debug("New Machine found")
            if(jobFound==True):
                #logger.debug(currentJilLine)
                if("owner:" in currentJilLine):
                    jobOwner=currentJilLine.partition("owner:")[2].strip()
                if("machine:" in currentJilLine):
                    jobMachine=currentJilLine.partition("machine:")[2].strip()
                if(len(jobOwner)!=0 and len(jobMachine)!=0 and len(jobName)!=0):
                    jobFound=False
                    jobMapDict[jobName]=jobOwner+":"+jobMachine
                    if(jobOwner+":"+jobMachine not in job_machine_owner_list):
                        job_machine_owner_list.append(jobOwner+":"+jobMachine)

        print(job_machine_owner_list)
        createJilDefinitions("C:\\Users\\kesav\\OneDrive - Robert Mark Technologies\\RMT-Arch\\UnionBank\\prod_connect.txt")

def createJilDefinitions(outputFile):
    logger = logging.getLogger("uboc.extract_info.createJilDefinitions")
    for item in job_machine_owner_list:
        logger.debug(item)
        connect_job_name="CONNECT_"+item.split(":")[1].strip()+"_"+item.split(":")[0].strip()
        logger.debug("Connect job name is: "+connect_job_name)
        write_to_file("insert_job: "+connect_job_name+"\n",outputFile)
        write_to_file("command: echo \"CONNECT TEST\""+"\n",outputFile)
        write_to_file("machine: "+item.split(":")[1].strip()+"\n",outputFile)
        write_to_file("owner: "+item.split(":")[0].strip()+"\n",outputFile)
        write_to_file(" "+"\n",outputFile)



main()