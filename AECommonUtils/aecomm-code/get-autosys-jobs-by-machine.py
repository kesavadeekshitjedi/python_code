'''
Created on Mar 8, 2018

@author: kesav
'''

import re
import logging
import logging.config

job_name_glb_list=[]
job_name_usr_list=[]

job_name_fnl_list=[]

jil_file_name=""
job_definition_dict = {}


def write_to_file(inputString,outputFile):
    logger=logging.getLogger("AECommonUtils.get-autosys-jobs-by-name.write_to_file")
    logger.info("test")
    fileWriter = open(outputFile, "a")
    fileWriter.write(inputString)

def main():
    logging.config.fileConfig("../config/logging.config")
    logger = logging.getLogger("AECommonUtils.get-autosys-jobs-by-machine.main")
    logger.info("Logging initialized....")
