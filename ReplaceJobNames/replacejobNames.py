
import re
from datetime import datetime
from shutil import copyfile
import time

def writeToFile(outputFile,jilLine):
	fileWriter=open(outputFile,"a")
	fileWriter.write(jilLine)

def readJilFileForRename(inputJil,outputJil,suffix):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    copyfile(inputJil,inputJil+".backup-"+timestamp)
    with open(inputJil) as myInputJil:
        for line in myInputJil:
            currentJilLine = line.strip()
            if("insert_job: " in currentJilLine):
                print("Job Definition line found")
                jobStringTuple = currentJilLine.split("insert_job:").strip()
                print(jobStringTuple)


def main():
