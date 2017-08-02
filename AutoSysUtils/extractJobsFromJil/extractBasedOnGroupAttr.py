import re
import logging
import logging.config


def readJil(jilInputFile,groupSearchString,topBoxName,topBoxCalendar,topBoxTime):
    jobName="";
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("JPMC-JMO-Analyzer.GeJobsWithGroupAttribute")
    logging.info("Reading {0} for {1]".format(jilInputFile,groupSearchString))
    with open(jilInputFile) as jilInput:
        for line in jilInput:
            currentJilLine=line.strip()
            if("insert_job" in currentJilLine):
                logger.debug("Job Line found")
                jobName=currentJilLine.partition("insert_job:")[2].partition("job_type:")[0].strip()
            groupAttribute="group: "+groupSearchString
            if(groupAttribute in currentJilLine):
                logger.info("Match found: {0} with Group: {1} ".format(jobName,groupSearchString))
                print("update_job: "+jobName)
                print("box_name: "+topBoxName)
                print("date_conditions: 1")
                print("start_times: "+topBoxTime)

def main():
    readJil("D:\\OneDrive-Business\\OneDrive - Robert Mark Technologies\\JPMC-JMO-Conversion\\JMO_Extracts\Phase4\\From_Hank\\2017.07.30\\TopBoxDisabled__NonODSEnabled\\JOBS_____.Tranche4.jil","ns_ods_heartbeat","d68.am.prebatch.maint.base.main.box","base","18:50")


main()