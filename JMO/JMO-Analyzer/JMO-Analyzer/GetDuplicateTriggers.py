import re
import logging
import logging.config

jobDefString = "DEFINE JOB ID="
jobsetDefString = "DEFINE JOBSET ID="
jobpredDefString = "DEFINE JOBPRED ID="
jobsetpredDefString = "DEFINE JOBSETPRED ID="
stationDefString = "DEFINE STATION ID="
triggerDefString = "DEFINE TRIGGER ID="
resourceDefString = "DEFINE RESOURCE ID="
jobresDefString = "DEFINE JOBRES ID="
jobsetresDefString = "DEFINE JOBSETRES ID="
stationgroupDefString = "DEFINE STATIONGROUP ID="
calendarDefString = "DEFINE CALENDAR ID="
jobparmDefString = "DEFINE JOBPARM ID="
critKeyString = "CRITKEYS="
critcalString = "CRITCAL="
critHolidayActionString = "CRITHACT="

triggerList=[]
duplicateTriggerList=[]

def main():
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("JPMC-JMO-Analyzer.GetDuplicateTriggerDefs.main")
    jmoExtractFile = input("Enter the full path to the JMO Extract: ")
    logger.info("Reading {0} ")
    with open(jmoExtractFile) as myJMOExtract:


        for line in myJMOExtract:
            currentLine = line.strip()
            if (re.match(triggerDefString, currentLine, flags=0)):

                logger.info("Trigger Definition found")
                logger.debug(currentLine)
                tempTriggerID = currentLine.partition(triggerDefString)[2].partition("DESCRIPTION=")[0].strip()
                myTriggerSplits = tempTriggerID.split(',')
                # logger.debug(myTriggerSplits)
                myTriggerID = myTriggerSplits[0].strip().replace('(', "")
                myTriggerType = myTriggerSplits[1].replace(')', "").strip()
                logger.debug("Adding Trigger: {0} to triggerList".format(myTriggerID))
                if(not myTriggerID in triggerList):
                    triggerList.append(myTriggerID)
                else:
                    logger.info("Duplicate Trigger Definition found: {0} {1}".format(currentLine,myTriggerID))
                    duplicateTriggerList.append(myTriggerID)

            if (re.match(calendarDefString, currentLine, flags=0)):

                logger.info("Calendar Definition found")
                logger.debug(currentLine)




main()
print("Hello")

for j in duplicateTriggerList:
    print("Duplicate trigger: {0}".format(j))