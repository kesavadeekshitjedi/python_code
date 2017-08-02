from lxml import etree
from xml.dom import minidom
import re
from datetime import datetime
import logging
import logging.config

def readXMLFile(xmlInput):
    logger=logging.getLogger("Entergy.AutoSysExtractor.readXMLFile")
    logger.info("reading xml input file {0}".format(xmlInput))
    doc=etree.parse(xmlInput)
    userFolderElement=doc.find('GlobalUser')
    #logger.info(userFolderElement.text)
    logger.info(userFolderElement.get('UserName'))
    logger.info(userFolderElement.get('FirstName'))
    logger.info(userFolderElement.get('LastName'))

def readXMLMinidom(xmlInput):
    logger=logging.getLogger("Entergy.AutoSysExtractor.readminidom")
    xmlDoc=minidom.parse(xmlInput)
    collection=xmlDoc.documentElement
    if collection.hasAttribute("GlobalUser"):
        logger.info(" Element: {0}",format(collection.getAttribute("UserName")))

def main():
     logging.config.fileConfig("logging.conf")
     logger=logging.getLogger("Entergy.AutoSysExtractor.MAIN")
     logger.info("Info Message")

main()
readXMLMinidom("D:\\Entergy-Files\\WCC0004.xml")