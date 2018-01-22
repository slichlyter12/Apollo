#!/usr/local/bin/python3.6

import os
import subprocess
import csv

IMPORT_FILE = 'usernames.csv'
FIELDNAMES = ['firstname', 'lastname', 'gid', 'osuid', 'url']

with open(IMPORT_FILE, newline='') as infile:
    reader = csv.DictReader(infile, fieldnames=FIELDNAMES)
    next(reader) # Skip over header
    for row in reader:
        dirname = row['osuid'] + "/dominion/"
        os.chdir(dirname)
        subprocess.run("make all", shell=True, check=True)
        subprocess.run("make clean", shell=True, check=True)
        os.chdir("../..")
