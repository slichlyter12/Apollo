#!/usr/local/bin/python3.6

import os
import subprocess
import csv

IMPORT_FILE = 'usernames.csv'
FIELDNAMES = ['firstname', 'lastname', 'gid', 'osuid', 'url']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open(IMPORT_FILE, newline='') as infile:
    reader = csv.DictReader(infile, fieldnames=FIELDNAMES)
    next(reader) # Skip over header
    for row in reader:

        failed_project = False
        failed_base = False

        # Build osuid/project/osuid/dominion
        dir = row['osuid'] + "/projects/" + row['osuid'] + "/dominion"
        try:
            os.chdir(dir)
            subprocess.run(["make", "all"])
            print(bcolors.OKGREEN + "Built: " + dir + bcolors.ENDC)
            subprocess.run(["make", "clean"])
            print(bcolors.OKGREEN + "Cleaned: " + dir + bcolors.ENDC)
            print("\n\n\n")
            os.chdir("../../../..")
        except:
            failed_project = True
            print(bcolors.WARNING + "WARNING: Could not build: " + dir + bcolors.ENDC)

        # Build and clean to check for compilation errors
        dir = row['osuid'] + "/dominion/"
        try:
            os.chdir(dir)
            subprocess.run(["make", "all"])
            print(bcolors.OKGREEN + "Built: " + dir + bcolors.ENDC)
            subprocess.run(["make", "clean"])
            print(bcolors.OKGREEN + "Cleaned: " + dir + bcolors.ENDC)
            print("\n\n\n")
            os.chdir("../../")
        except:
            failed_base = True
            print(bcolors.WARNING + "WARNING: Could not build: " + dir + bcolors.ENDC)

        # Print what failed
        if failed_project:
            print(bcolors.FAIL + "Failed Project Build" + bcolors.ENDC)
        if failed_base:
            print(bcolors.FAIL + "Failed Base Build" + bcolors.ENDC)
