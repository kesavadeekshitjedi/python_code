import re
from subprocess import call

def main():
    print("reading Autosys machine counts")
    autorepString="autorep -M ALL -q"
    call([autorepString])

