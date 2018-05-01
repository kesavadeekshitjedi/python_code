import logging
import logging.config
from shutil import copyfile
import time
from datetime import datetime
import re
import os


file_name_list=[] # Contains the list of filenames in the folder.
instance_name_list=[]
instance_job_list_Dict = {}
GOLDMAN_FILE_FOLDER="D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\Goldman\\files\\Prod_neededFiles\\"

def writeToFile(outputFile,sourceString):
    fileWriter=open(outputFile,"a")
    fileWriter.write(sourceString)


def getFileList(FileFolder):
    file_name_list=os.listdir(FileFolder)
    print(file_name_list)
    for currentFileName in file_name_list:
        fullFileName="D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\\Goldman\\files\\Prod_neededFiles\\"+currentFileName
        instance_name=currentFileName.split("_")[0]
        print("Extracting information for {0} from {1}".format(instance_name,fullFileName))
        with open(fullFileName) as GS_FILE:
            for line in GS_FILE:
                jobName=line.split(" ")[1]
                #print("Job Name is: ",jobName)
                writeToFile("D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\\Goldman\\files\\aggregates\\"+instance_name+".jobs.txt",jobName+"\n")
def getInstanceNameFromFile():
    fileName="PAR_Jobs2migrate.txt.GS"
    instanceName=fileName.split("_")
    print("Instance Name is {0}  ".format(instanceName[0]))
def main():
    getFileList("D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\\Goldman\\files\\Prod_neededFiles")


main()