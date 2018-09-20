import requests
from requests.auth import HTTPBasicAuth
import json
import getpass
import collections

ae_websrv_url = "https://10.0.1.73:9443/AEWS/job.json"
myResponse = requests.get(ae_websrv_url,auth=HTTPBasicAuth(input("username: "),getpass.getpass("password: ")),verify=False)
'if we get HTTP 200'
if(myResponse.ok):
    parsed_json=json.loads(myResponse.content)
    jobNames=[]
    for k,v in parsed_json.items():
        for jobName in v:
            if("name" in jobName):
                #print(jobName['name'])
                jobNames.append(jobName['name'])
    

    for myJob in jobNames:
        print("Job Name: {0}".format(myJob))