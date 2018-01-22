#!/usr/local/bin/python3.6

import os
import subprocess
import re
import csv
from git import Repo

IMPORT_FILE = 'usernames.csv'
FIELDNAMES = ['firstname', 'lastname', 'gid', 'osuid', 'url']
ASSIGNMENT_NUM = '1'

with open(IMPORT_FILE, newline='') as infile:
    reader = csv.DictReader(infile, fieldnames=FIELDNAMES)
    next(reader) # Skip over header
    for row in reader:

        # Get repo and branch
        repo_name = row['url']
        branch_name = row['osuid'] + '-assignment-' + ASSIGNMENT_NUM

        # Check if repo exists, if so pull, if not clone
        if not (os.path.exists(row['osuid'])):
            # Clone
            os.mkdir(row['osuid'])
            Repo.clone_from(repo_name, row['osuid'])

        # Switch to desired branch
        os.chdir(row['osuid'])
        repo = Repo()
        git = repo.git
        git.checkout(branch_name)

