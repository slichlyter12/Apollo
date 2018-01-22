#!/usr/local/bin/python3.6

import csv

IMPORT_FILE = 'usernames.csv'
FIELDNAMES = ['firstname', 'lastname', 'id', 'url']

with open(IMPORT_FILE, newline='') as infile:
    reader = csv.DictReader(infile, fieldnames=FIELDNAMES, dialect='excel')
    next(reader) # Skip over header
    for row in reader:
        print(row['firstname'], row['lastname'], row['id'], row['url'])
