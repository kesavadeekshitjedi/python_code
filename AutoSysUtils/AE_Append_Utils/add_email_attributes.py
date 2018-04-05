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
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs.jil", line)
            writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs.jil","")
            if ("description" in line):
                description_attribute = line.partition("description:")[2].strip()

                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs.jil", "send_notification: F \n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs.jil",
                        "notification_msg: {0}".format(description_attribute) + "\n")
                writeToFile("D:\\Fastenal-PSAdapter-Jobs\\JobsWithEmailAttribs.jil",
                        "notification_emailaddress: iscomputeroperations@fastenal.com \n")


def main():
    readJil("D:\\Fastenal-PSAdapter-Jobs\\AllJobs.jil")

main()