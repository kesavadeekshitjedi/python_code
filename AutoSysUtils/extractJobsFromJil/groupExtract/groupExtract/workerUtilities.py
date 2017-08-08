import re
import logging
import pypyodbc
import logging.config

def writeToFile(outputFile, line):
    fileWriter = open(outputFile,"a")
    fileWriter.write(line+"\n")



    
def createSQLConnection(sqlServerHost,sqlServerPort,sqlServerUser,sqlServerPass,sqlServerDB):
    logging.config.fileConfig("logging.conf")
    logging.getLogger("ACCEConfiguration.createSQLConnection")
    logging.info("Connecting to SQL Server...")
    con = pypyodbc.connect('DRIVER={SQL Server};SERVER=Prod1\SQL2008R2;DATABASE=SDE;UID=sa;PWD=sa')

