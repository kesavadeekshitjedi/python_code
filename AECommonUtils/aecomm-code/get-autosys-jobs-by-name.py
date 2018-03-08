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

def read_jobaname_file(jobNameFile):
    logger=logging.getLogger("AECommonUtils.get-autosys-jobs-by-name.read_jobaname_file")
    logger.info("Attempting to open file: "+jobNameFile)
    with open(jobNameFile) as job_name_list:
        for current_jobname_line in job_name_list:
            job_name_glb_list.append(current_jobname_line.strip())
    
    
    for job_name in job_name_glb_list:
        logger.debug("Job Name Collected \"{0}\" ".format(job_name))
     
    

def read_jil_to_extract_jobs(jil_file_name,job_name_glb_list):        
    logger=logging.getLogger("AECommonUtils.get-autosys-jobs-by-name.read_jil_to_extract_jobs")
    found_job=False
    with open(jil_file_name) as jil_def_file:
        for current_jil_line in jil_def_file:
            
            if("insert_job" in current_jil_line):
                current_job_name=current_jil_line.partition("insert_job:")[2].partition("job_type:")[0].strip()
                logger.debug("Job Name: "+current_job_name)
                if(current_job_name in job_name_glb_list):
                    logger.info("Found job to extract. Extracting job "+current_job_name)
                    job_name_glb_list.remove(current_job_name)
                    print(job_name_glb_list)
                    found_job = True
                else: 
                    found_job=False
            if(current_jil_line==" \n"):
                found_job=False
                    
            if(found_job==True and "/*" not in current_jil_line):
                print(current_jil_line.strip())
                write_to_file(current_jil_line, "D:\\Python-Utils\\AECommonUtils-Properties\\outFile.txt")
            
                    
                    
                
    
    
def read_jobnames_listobject(job_list):
     logger=logging.getLogger("AECommonUtils.get-autosys-jobs-by-name.read_jobnames_listobject")
     logger.info("Attempting to read jobnames list: ",job_list)
    
def read_common_properties(properties_file):
    logger = logging.getLogger("AECommonUtils.get-autosys-jobs-by-name.read_common_properties")
    
                               
def main():
    logging.config.fileConfig("../config/logging.config")
    logger = logging.getLogger("AECommonUtils.get-autosys-jobs-by-name.main")
    logger.info("Logging initialized....")
    logger.info("Reading properties file for information...")
    with open("../config/utils.properties") as properties_file:
        for current_prop_line in properties_file:
            if("JOBNAME_FILE_LIST" in current_prop_line):
                logger.debug(current_prop_line)
                job_name_file_path=current_prop_line[19:]
                logger.debug("File path: "+job_name_file_path)
            if("JILFILE_PATH" in current_prop_line):
                jil_file_name=current_prop_line[13:]
                logger.debug("Jil file path: "+jil_file_name)
                
    #write_to_file("blah", "D:\\Python-Utils\\AECommonUtils-Properties\\bla.txt")
    read_jobaname_file("D:\\Python-Utils\\AECommonUtils-Properties\\jobnames.txt")
    read_jil_to_extract_jobs("D:\\Python-Utils\\AECommonUtils-Properties\\jobs.txt", job_name_glb_list)
    
main()