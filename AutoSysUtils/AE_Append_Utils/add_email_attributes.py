job_found=False
first_pass = True

def writeToFile(outputFile, line):
    fileWriter = open(outputFile,"a")
    fileWriter.write(line)

def readJil(jilFileInput):
    with open(jilFileInput) as jilInput:
        for line in jilInput:
            print(line.strip())
            description_attribute = ""
            if("insert_job: " in line):


                print("New job definition found")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", " \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", " \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", line)
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "alarm_if_fail: 1 \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "alarm_if_terminated: 1 \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "notification_template: \"email1\" \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "notification_alarm_types: ALL \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "send_notification: F \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "notification_emailaddress: iscomputeroperations@fastenal.com \n")
                global job_found
                job_found=True

            else:
                if(len(line.strip()) != 0 and job_found==True):
                    if("notification_msg"  in line):
                        writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "notification_msg: \n ")
                    '''else:
                        writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", line)
                    '''

                if ("description" in line):
                    description_attribute = line.partition("description:")[2].strip()
                    # Adding the alarm and template information for Fastenal after upgrading to SP7

                    writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs2.jil", "#notification_msg: {0}".format(description_attribute) + "\n")




def main():
    readJil("D:\\Fastenal-PSAdapter-Jobs\\jobs05172018.txt")

main()