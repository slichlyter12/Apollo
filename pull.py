#!/usr/local/bin/python3.6

import os
from sys import argv
import csv
from git import Repo

IMPORT_FILE = 'usernames.csv'
FIELDNAMES = ['firstname', 'lastname', 'gid', 'osuid', 'url']
ASSIGNMENT_NUM = '1'


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


def pull():
    with open(IMPORT_FILE, newline='') as infile:
        reader = csv.DictReader(infile, fieldnames=FIELDNAMES)
        next(reader) # Skip over header
        for row in reader:

            # Get repo and branch
            repo_name = row['url']
            branch_name = row['osuid'] + '-assignment-' + ASSIGNMENT_NUM
            # branch_name = row['osuid'] + '-random-quiz'

            # Check if repo exists, if so pull, if not clone
            if not (os.path.exists(row['osuid'])):
                # Clone
                os.mkdir(row['osuid'])
                Repo.clone_from(repo_name, row['osuid'])

            # Switch to desired branch
            os.chdir(row['osuid'])
            repo = Repo()
            git = repo.git
            try:
                git.pull()
                git.checkout(branch_name)
                print(bcolors.OKGREEN + "Pulling: " + branch_name + bcolors.ENDC)
            except:
                print(bcolors.FAIL + "FAILED TO PULL: " + branch_name + bcolors.ENDC)

            # Check branch
            branch = repo.active_branch
            if (branch.name != branch_name):
                print(bcolors.WARNING + "Incorrect Branch: " + row["firstname"] + " " + row["lastname"] + bcolors.ENDC)

            # Switch back to main directory
            os.chdir("..")


if __name__ == "__main__":
    args = getopts(argv)
    if '-a' in args:
        ASSIGNMENT_NUM = args['-a']
    if '-i' in args:
        IMPORT_FILE = args['-i']
    pull()
