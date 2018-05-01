import re
import logging
import logging.config
from datetime import datetime
import time
import os
import collections
from collections import defaultdict

def main():
    # Initialize logging
    logging.config.fileConfig("resources/logging.conf")
    logger=logging.getLogger("archive_reader_main")
    logger.info("Logging Initialized....")

main()