#!/usr/local/bin/python3.6


import os
from sys import argv
import subprocess
import csv

from build import build

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


# Credit: https://gist.github.com/dideler/2395703
def getopts(args):
    opts = {}
    while args:
        if args[0][0] == '-':
            opts[args[0]] = args[1]
        args = args[1:]
    return opts


def test(dir, osuid):
    failed = False
    try:
        # Move to directory
        os.chdir(dir)

        # Run test code
        subprocess.run(["make", "randomtestcard1.out"])
        subprocess.run(["make", "randomtestcard1.out"])
        subprocess.run(["make", "randomtestadventurer.out"])

        # Get out path
        depth = dir.count('/')
        path = ""
        for _ in range(depth):
            path += "../"

        # Check if reports path exists, if not create it
        reports_path = path + "reports/"
        if not (os.path.exists(reports_path)):
            os.mkdir(reports_path)

        # Copy .out file to MAIN/reports
        subprocess.run(["cp", "*.out", reports_path + osuid + "_report.out"])

        # Clean directory
        subprocess.run(["make", "clean", "-s"])

        # Get out
        os.chdir(path)

    except:
        failed = True
        print(bcolors.WARNING + "WARNING: Could not test: " + dir + bcolors.ENDC)

    return failed


def main():
    with open(IMPORT_FILE, newline='') as infile:
        reader = csv.DictReader(infile, fieldnames=FIELDNAMES)
        next(reader) # Skip over header
        for row in reader:

            # Test osuid/project/osuid/dominion
            dir = row['osuid'] + "/projects/" + row['osuid'] + "/dominion/"
            build(dir, False)
            failed_project = test(dir, row['osuid'])

            # Test main dominion folder
            dir = row['osuid'] + "/dominion/"
            build(dir, False)
            failed_base = test(dir, row['osuid'])

            # Print what failed
            if failed_project:
                print(bcolors.FAIL + "Failed Project Test: " + row['osuid'] + bcolors.ENDC)
            if failed_base:
                print(bcolors.FAIL + "Failed Base Test: " + row['osuid'] + bcolors.ENDC)


if __name__ == "__main__":
    args = getopts(argv)
    if 'i' in args:
        IMPORT_FILE = args['-i']
    main()
