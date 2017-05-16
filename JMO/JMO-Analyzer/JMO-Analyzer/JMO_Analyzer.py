import re
from datetime import datetime
import logging
import logging.config


jobparmDefString="DEFINE JOBPARM ID="
splitJobsFile="D:\\JPMC-JMO\\extracts\\combined\\JobsFile.txt"
splitStationsFile="D:\\JPMC-JMO\\extracts\\combined\\StationsFile.txt"
splitJobsetFile="D:\\JPMC-JMO\\extracts\\combined\\JobsetsFile.txt"
splitTriggersFile="D:\\JPMC-JMO\\extracts\\combined\\TriggersFile.txt"
splitResourceFile="D:\\JPMC-JMO\\extracts\\combined\\ResourcesFile.txt"
splitCalendarsFile="D:\\JPMC-JMO\\extracts\\combined\\CalendarsFile.txt"
splitJobParmsFile="D:\\JPMC-JMO\\extracts\\combined\\JobParmsFile.txt"
def main():
    logging.config.fileConfig("logging.config")
    logger=logging.getLogger("JMOAnalyzer.main")
    logger.info("Logging initialized successfully...")
    logger.debug("test write to file")
    logger.info("Testing write to file info")
    splitJMOFilesIntoObjects("D:\\JPMC-JMO\\extracts\\combined\\AllPhases_05152017_P1P2P3.txt")
    logger.info("File Split Complete.")

def writeToFile(targetString, targetFile):
    logger=logging.getLogger("JMOAnalyzer.writeToFile")
    fileWriter = open(targetFile, "a")
    #logger.debug(targetString)
    fileWriter.write(targetString + "\n")

def splitJMOFilesIntoObjects(jmoSource):
    logger=logging.getLogger("JMOAnalyzer.splitJMOFiles")
    logger.info("Splitting {0} into seperate files that contain ".format(jmoSource))
    logger.info("1. JMO Jobs")
    logger.info("2. JMO Jobsets")
    logger.info("3. Calendar Definitions")
    logger.info("4. Station/Station Group Definitions")
    logger.info("5. Resource Definitions")
    logger.info("6. Job Parameters ")
    logger.info("7. Trigger Definitions")
    with open(jmoSource) as jmoSourceFileReader:
        for line in jmoSourceFileReader:
            currentLine=line.strip()
            logger.debug(currentLine)
            if(re.match("DEFINE STATION",currentLine,flags=0)):
                logger.debug("Station Definition found. Writing to Station file")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\StationsFile.txt")
            if(re.match("DEFINE STATIONGROUP",currentLine,flags=0)):
                logger.debug("Station Group Definition found. Writing to Station file")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\StationsFile.txt")
            if(re.match("DEFINE JOB ID",currentLine,flags=0)):
                logger.debug("Job Definition found")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\JobsFile.txt")
            if(re.match("DEFINE JOBSET ID=",currentLine,flags=0)):
                logger.debug("Jobset Definition found.")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\JobsetsFile.txt")
            if(re.match("DEFINE CAL ID",currentLine,flags=0)):
                logger.debug("Calendar Definition Found.")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\CalendarFile.txt")
            if(re.match("DEFINE RESOURCE ID=",currentLine,flags=0)):
                logger.debug("Resource Definition found.")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\ResourcesFile.txt")
            if(re.match("DEFINE TRIGGER ID=",currentLine,flags=0)):
                logger.debug("Trigger Definition Found.")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\TriggersFile.txt")
            if(jobparmDefString in currentLine or "PARM1" in currentLine or "PARM2" in currentLine or "PARM3" in currentLine or "PARM4" in currentLine or "PARM5" in currentLine or "PARM6" in currentLine or "PARM7" in currentLine or "PARM8" in currentLine or "PARM9" in currentLine or "PARM10" in currentLine or "PARM11" in currentLine or "PARM12" in currentLine or "PARM13" in currentLine or "PARM14" in currentLine or "PARM15" in currentLine or "PARM16" in currentLine or "PARM17" in currentLine or "PARM18" in currentLine or "PARM19" in currentLine or "PARM20" in currentLine or "PARM21" in currentLine or "PARM22" in currentLine):
                logger.debug("Job Parm line found")
                writeToFile(currentLine,"D:\\JPMC-JMO\\extracts\\combined\\JobParmsFile.txt")

main()