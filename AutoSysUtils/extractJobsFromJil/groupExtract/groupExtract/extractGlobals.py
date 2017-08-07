import logging
import logging.config
import re
from datetime import datetime
from workerUtilities import writeToFile

def createGlobalsExport(globalImportFile):
    with open(globalImportFile) as myGlobalVarInput:
        for globalLine in myGlobalVarInput:
            globalVarName=""
            globalVarValue=""
            currentLine=globalLine.strip()
            globalTuple=currentLine.split((' '))
            globalVarName=globalTuple[0].strip()
            globalVarValue=globalTuple[1].strip()
            #print("Variable Name: "+globalVarName)
            #print("Variable Value: "+globalVarValue)
            myLine="sendevent -E SET_GLOBAL -G "+globalVarName+"="+globalVarValue
            print(myLine)
            writeToFile(myLine,"D:\\exportGlobalsFile_Harris.txt")

