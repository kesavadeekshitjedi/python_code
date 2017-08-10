import re
import logging
#import pypyodbc
import logging.config
import os
import cx_Oracle
import collections
from collections import defaultdict

jobConditionMap=defaultdict(list)
dbConnection=None

def writeToFile(outputFile, line):
    file_folder=os.path.dirname(outputFile)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    try:
       
        fileWriter=open(outputFile,"a")
    except FileNotFoundError:

        fileWriter = open(outputFile,"w")
    fileWriter.write(line+"\n")


def getConditionsForJob(oracleServerhost,oracleServerPort,username,password,oracleSID,jobName):
    logger=logging.getLogger("JMO_AE_Utils.groupExtract.getConditionsForJob")
    logger.info("Getting conditions for job: {0} ".format(jobName))
    logger.info("Establishing database connection...")
    dbTNS=cx_Oracle.makedsn(oracleServerhost,oracleServerPort,oracleSID)
    logger.info("TNS Entry is: "+dbTNS)
    try:
        conditionJobVals=[]
        conditionJobList=[]
        global dbConnection
        dbConnection = cx_Oracle.connect(username,password,dbTNS)
        logger.info("Oracle connection sucecssfully established. Oracle version: "+dbConnection.version)
        myOraCursor=dbConnection.cursor()
        # Cursor created here
        myJOIDSQLString="select joid from ujo_job where job_name='"+jobName+"' and is_active=1 and is_currver=1"
        logger.info("Current Query: {0}".format(myJOIDSQLString))
        myOraCursor.execute(myJOIDSQLString)
        for row in myOraCursor:
            joid=row[0]
            logger.debug("JOID for Job: {0} is ".format(joid))
        # Close the cursor here
        myOraCursor.close()
        myOraCursor2=dbConnection.cursor()
        mycondSQLString="select cond_job_name from ujo_job_cond where joid='"+str(joid)+"'"
        
        myOraCursor2.execute(mycondSQLString)
        for row2 in myOraCursor2:
            condJobName=row2[0]
            if condJobName is not None:
                
                logger.debug("Cond Job: "+condJobName)
                if(not condJobName in conditionJobList):
                    conditionJobList.append(condJobName)
                    jobConditionMap[jobName]=conditionJobList
            
    finally:
        dbConnection.close()


def getCalendarsForJob(oracleServerhost,oracleServerPort,username,password,oracleSID,jobName):
    joid=""
    
    logger.info("Connecting to DB...")
    logger=logging.getLogger("JMO_AE_Utils.workerUtilities.createSQLServerConnection")
    logger.info("Attempting to connect to Oracle Server: {0} and DB {1}".format(oracleServerhost,oracleSID))
    # Establish connection to the Oracle database
    