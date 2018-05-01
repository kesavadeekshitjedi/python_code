import re
import logging
import os
import logging.config
from datetime import datetime


file_name_list=[] # Contains the list of filenames in the folder.
instance_name_list=[]
instance_job_list_Dict = {}
GOLDMAN_JIL_FILE_FOLDER="D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\\Goldman\\files\\PRD_Files_01-24-2018\extracts\\"
GOLDMAN_REPORT_FOLDER="D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\Goldman\\Reports\\"
outputFolder="D:\\JilExtracts"
CustomerName="Goldman-Sachs"
cmd_job_list=[]
fw_job_list=[]
box_job_list=[]



def writeToFile(inputString,outputFile):
    fileWriter = open(outputFile, "a")
    fileWriter.write(inputString)


def main():
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("Goldman_Extractors.GS_Analysis.main")
    logger.info("Testing message")

    getInstanceFiles()

def getInstanceFiles():
    # This method is a heler method that gets the list of files in the GS load folder.
    # The instance files contain the Job Definitions that have been marked as "Good for migration" , using the ArchiveUtils.jar
    # Once the files are found, then [ass them as input to the readInstanceFiles method to create a dictionary .

    logger=logging.getLogger("Goldman_Extractors.GS_Analysis.getInstanceFiles")
    file_name_list = os.listdir(GOLDMAN_JIL_FILE_FOLDER)
    #print(file_name_list)
    readInstanceFiles(file_name_list)

def readInstanceFiles(fileNameListObject):
    # App Code = the word before the first occurance of "." or "_" or "-".
    # For each App Code, gather the list of jobs (cmd, fw and box)
    #   If the current job has a dependency on another job, then store the dependent job and its condition in the conditionMap
    # For each App Code, read the excel sheet to get the DID
    # Provide counts based on the DID information

    foundJob=False
    cmdJobCount=0
    boxJobCount=0
    fwJobCount=0
    total_job_count=0
    jobDefList = []
    logger = logging.getLogger("Goldman_Extractors.GS_Analysis.readInstanceFiles")
    logger.info("Reading the fileNameListObject to get the list of files")
    report_folder = GOLDMAN_REPORT_FOLDER + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"\\"+CustomerName
    os.makedirs(report_folder)
    outputFile = report_folder + "\\" + "JobCount_Report.txt"
    writeToFile("               CMD Job Count      BOX JOB COUNT       FW JOB COUNT        Total \n", outputFile)
    for file in fileNameListObject:
        instanceName=file.split(".")[0].strip()
        logger.info("Instance Name is: "+instanceName)
        logger.info("Reading file: "+file)


        logger.info("Writing Report to "+outputFile)
        with open(GOLDMAN_JIL_FILE_FOLDER+"\\"+file) as GS_FILE:
            for currentJilLine in GS_FILE:
                if("insert_job" in currentJilLine):
                    logger.debug("Job Found")
                    foundJob=True
                    jobName = currentJilLine.partition("insert_job:")[2].partition("job_type:")[0].strip() # Getting job name.
                    jobType = currentJilLine.partition("job_type:")[2].strip() # Gets the job type
                    logger.info(jobName+":"+jobType)
                    if(jobType=="c"):
                        cmdJobCount=cmdJobCount+1
                        cmd_job_list.append(instanceName+":"+jobName)
                    if(jobType=="f"):

                        fwJobCount=fwJobCount+1
                        fw_job_list.append(instanceName+":"+jobName)

                    if (jobType == "b"):
                        boxJobCount = boxJobCount + 1
                        box_job_list.append(instanceName + ":" + jobName)

                if(foundJob==True):
                    jobDefList.append(currentJilLine)
            if("box_name" in jobDefList):
                print("job belongs to box")
        total_job_count=cmdJobCount+fwJobCount+boxJobCount
        output_line=instanceName+"              "+str(cmdJobCount)+"                 "+str(boxJobCount)+"                "+str(fwJobCount)+"                "+str(total_job_count)
        writeToFile(output_line+"\n",outputFile)
        logger.info("Done analyzing "+file)

        jobList = []
        jobList.append("PWMREP_DC1_CCR_MRG")
        jobList.append("CLSVGSI_GSI_QUEUE_MNTR_BOX")
        readJobNamesList(GOLDMAN_JIL_FILE_FOLDER+"\\CT1.jil",jobList)
def findAnomalies(fileNameListObject):
    logger=logging.getLogger("Goldman_Extractors.GS_Analysis.findAnomalies")

def readJobNamesList(inputFile, jobList):
    jobDefinitionList = []
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
                jobDefinitionList.append(currentJilLine)
            elif(currentJilLine=="\n"):
                jobFound=False


main()