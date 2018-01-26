#!/usr/local/bin/python3.6

import os
from sys import argv
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


# Credit: https://gist.github.com/dideler/2395703
def getopts(args):
    opts = {}
    while args:
        if args[0][0] == '-':
            opts[args[0]] = args[1]
        args = args[1:]
    return opts


def build(dir, failed):
    try:
        # Move to directory
        os.chdir(dir)

        # Modify Makefile to suppress warnings
        with open("Makefile", "r+") as makefile:
            flags = makefile.readline()
            flags = flags[:-1] + " -w\n\n"
            makefile.seek(0, 0)
            makefile.write(flags)

        # Make and clean
        subprocess.run(["make", "all", "-s"])
        print(bcolors.OKGREEN + "Built: " + dir + bcolors.ENDC)
        subprocess.run(["make", "clean", "-s"])
        # print(bcolors.OKGREEN + "Cleaned: " + dir + bcolors.ENDC)

        # Change Makefile back to original
        subprocess.run(["git", "checkout", "Makefile"])

        # Get out of there
        depth = dir.count('/')
        path = ""
        for _ in range(depth):
            path += "../"
        os.chdir(path)

    except:
        failed = True
        print(bcolors.WARNING + "WARNING: Could not build: " + dir + bcolors.ENDC)

    return failed


def main():
    with open(IMPORT_FILE, newline='') as infile:
        reader = csv.DictReader(infile, fieldnames=FIELDNAMES)
        next(reader) # Skip over header
        for row in reader:

            failed_project = False
            failed_base = False

            # Build osuid/project/osuid/dominion
            dir = row['osuid'] + "/projects/" + row['osuid'] + "/dominion/"
            failed_project = build(dir, failed_project)

            # Build and clean to check for compilation errors
            dir = row['osuid'] + "/dominion/"
            failed_base = build(dir, failed_base)

            # Print what failed
            if failed_project:
                print(bcolors.FAIL + "Failed Project Build: " + row['osuid'] + bcolors.ENDC)
            if failed_base:
                print(bcolors.FAIL + "Failed Base Build: " + row['osuid'] + bcolors.ENDC)


if __name__ == "__main__":
    args = getopts(argv)
    if 'i' in args:
        IMPORT_FILE = args['-i']
    main()