import requests
from requests.auth import HTTPBasicAuth
from argparse import ArgumentParser
from xml.etree import ElementTree as ET

import getpass

ae_websrv_url = "https://10.0.1.73:9443/AEWS/job.xml"
myResponse = requests.get(ae_websrv_url,auth=HTTPBasicAuth(input("username: "),getpass.getpass("password: ")),verify=False)
'if we get HTTP 200'
if(myResponse.ok):
    
    jobNames=[]
    xmlData = myResponse.content
    with open('restoutput.xml','wb') as f:
        f.write(myResponse.content)
    tree = ET.fromstring(myResponse.content)
    for child in tree.iter('*'):
        #print("Tag: {0}, Text: {1}".format(child.tag,child.text))
        if(child.tag=="name"):
            jobNames.append(child.text)
    for jobName in jobNames:
        print("Job Name: "+jobName)



    
    
