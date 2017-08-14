import re
import logging
import logging.config
from datetime import datetime
import time
import os
import collections
from collections import defaultdict
import xlrd
import JilUtilities
from JilUtilities import readJil
from JilUtilities import readJilForCommandAndCondition
from JilUtilities import readJilForBoxLevelStructure
import groupExtract
from groupExtract import *
import copyJobStatus
from copyJobStatus import *
from workerUtilities import *



jobConditionMapMain=defaultdict(list)

# This will be the main module from where all other modules will be imported and called as methods.
# DK - 04/08/2017
# DK - 04/08/2017 - Sub boxes shouldnt have date conditions and calendars.Only top box should
# As of 08/04/2017 - Top Box needs to be created manually. Looking to fix this.


def main():
    logging.config.fileConfig("logging.conf")
    logger=logging.getLogger("JMO_AE_Utils.main")
    print("1. Read JIL File and create missing machine and resource defs")
    print("2. Read Excel sheet to create Top Level Boxes")
    print("3. Read jil and extract command and condition for update_job file")
    print("4. Copy Job Status")
    print("5. Set Filewatchers in top level box by Calendar.")
    user_choice=input("Select an option (1) or (2) or (3) or (4).")
    if(user_choice=="1"):
   
        readJil("C:\\JMOFiles\\JOBS_____.Tranche4.jil","D:\JPMC-JMO\\scripted_outputFiles\\Resources.jil","D:\JPMC-JMO\\scripted_outputFiles\\Machines.jil")
        readJil("C:\\JMOFiles\\JOBS_____.ONDMD.Tranche4.jil","D:\JPMC-JMO\\scripted_outputFiles\\Resources_ONDMD.jil","D:\JPMC-JMO\\scripted_outputFiles\\Machines_ONDMD.jil")
        logger.info("Done")  
    
    if(user_choice=="2"):
        currentTime=time.strftime("%Y%m%d-%H%M%S")
        readExcelForTopLevel("C:\\JMOFiles\\Tranche4JobstoBeConverted-Final.xlsx","Sheet1")
        print(type(jobsetsInTopBox))
        keyList=jobsetsInTopBox.keys()
        print(type(keyList))
        boxStartTime="";
        boxCalendar="";
        myKeyList=list(keyList)
        for key in myKeyList:
            keyValues=jobsetsInTopBox[key]
            for kvalue in keyValues:
                logger.debug("Value for Key: {0} is {1} ".format(key,kvalue))
                kvTuple=kvalue.split('-')
                logger.info(kvTuple)
                boxStartTime=kvTuple[1].strip()
                boxCalendar=kvTuple[2].strip()
                readJilForGroup("c:\\jmofiles\\JOBS_____.Tranche4.jil",kvTuple[0],key,kvTuple[2],kvTuple[1])
            # Creating the TopBoxes here.
            writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBoxFile_"+currentTime+".txt" ,"insert_job: "+key)
            writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBoxFile_"+currentTime+".txt","job_type: BOX")
            writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBoxFile_"+currentTime+".txt","date_conditions: 1")
            writeToFile("C:\\JMOFiles\\TopBoxFiles\\TopBoxFile_"+currentTime+".txt","start_times: \""+boxStartTime+"\"")
            writeToFile("C:\\JMOFiles\\TopBoxFile.txt","run_calendar: "+boxCalendar)
    if(user_choice=="3"):
        jilFileName=input("Enter the full path to the jil file to read")
        readJilForBoxLevelStructure(jilFileName,"*")
        readJilForCommandAndCondition(jilFileName)
    if(user_choice=="4"):
        readJilFile("D:\\autosysstatus\\jobstatus.txt")
        writeUpdatedJobStatusFile("D:\\autosysstatus\\jobdef.txt")
    if(user_choice=="5"):
        readJilForFileWatchers("C:\\JMOFiles\\FTJobs_JPMC.txt","0")
    if(user_choice=="6"):
        p=Properties()
        p.load(open("C:\\JMOFiles\\jmo2ae.properties"))
        p.list()
        p.items()
        print(p[database.hostname])
        getConditionsForJob("LUMOS","1521","aedbadmin","Test1234","SP3","cbos.perform.monthly.batch.check.008.r")
        #createOracleConnection("LUMOS","1521","aedbadmin","Test1234","SP3")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_ods_heartbeat","d68.am.prebatch.maint.base.main.box","base","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_pentaho_carte_reboot","d68.am.prebatch.maint.base.main.box","base","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_gwm_uscore_bus_sys_partition","d68.am.prebatch.maint.us_cmpl.main.box","us_cmpl","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_internal_truncate","d68.am.prebatch.maint.us_cmpl.main.box","us_cmpl","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_mw_stp_archive","d68.am.prebatch.maint.us_mf_fd.main.box","us_mf_fd","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_ods_ao_batch","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_ods_cs_proc_dt","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_acats_extracts","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_add_partition_daily","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_calendar","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_gstp_add_partition_daily","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_gstp_add_partition_daily_ws","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_internal_add_partition_daily","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_pb_sac","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_truncate","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_uscore_add_partition_daily","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    #readJil("c:\\jmofiles\\JOBS_____.Tranche4.jil","ns_pbds_uscore_pb_sac","d68.am.prebatch.maint.usmffdsx.main.box","usmffdsx","18:45")
    logger.info("Done")

main()