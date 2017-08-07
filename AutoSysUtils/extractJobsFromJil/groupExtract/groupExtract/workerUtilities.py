import re
import logging
import logging.config

def writeToFile(outputFile, line):
    fileWriter = open(outputFile,"a")
    fileWriter.write(line+"\n")


