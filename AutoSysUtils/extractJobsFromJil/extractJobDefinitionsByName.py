import logging
import logging.config


def writeToFile(outputFile,jilLine):
	fileWriter=open(outputFile,"a")
	fileWriter.write(jilLine)

def main():
    logging.config.fileConfig("logging.conf")
    logging.info("Test message")

main()