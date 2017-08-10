import re
import logging
#import pypyodbc
import logging.config
import os

def writeToFile(outputFile, line):
    file_folder=os.path.dirname(outputFile)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    try:
       
        fileWriter=open(outputFile,"a")
    except FileNotFoundError:

        fileWriter = open(outputFile,"w")
    fileWriter.write(line+"\n")



    
def createSQLConnection(sqlServerHost,sqlServerPort,sqlServerUser,sqlServerPass,sqlServerDB):
    logging.config.fileConfig("logging.conf")
    logging.getLogger("ACCEConfiguration.createSQLConnection")
    logging.info("Connecting to SQL Server...")
    con = pypyodbc.connect('DRIVER={SQL Server};SERVER=Prod1\SQL2008R2;DATABASE=SDE;UID=sa;PWD=sa')

