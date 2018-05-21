
job_type=""
job_name=""
job_description=""

def writeToFile(outputFile, line):
    fileWriter = open(outputFile,"a")
    fileWriter.write(line)

def readJil(jilFileInput):
    with open(jilFileInput) as jilInput:
        for line in jilInput:
            print(line)
            global job_type
            global job_name
            global job_description
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", line)
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "alarm_if_fail: 1 \n")
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "alarm_if_terminated: 1 \n")
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil",

                        "notification_template: \"email1\" \n")
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "notification_alarm_types: ALL \n")
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "send_notification: F \n")
            if ("insert_job: " in line):
                print("New Job found...getting job type")

                job_name=line.partition("insert_job: ")[2].partition("job_type:")[0].strip()
                job_type=line.partition("job_type:")[2].strip()

            if("description:" in line):

                job_description=line.partition("description:")[2].strip()
                print(" Job: {0} is of type: {1} and has description: {2} ".format(job_name, job_type, job_description))


                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "#notification_msg: {0}".format(job_description) + "\n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "notification_emailaddress: iscomputeroperations@fastenal.com \n")
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", " \n")


def main():
    readJil("D:\\Fastenal-PSAdapter-Jobs\\jobs05172018.txt")

main()