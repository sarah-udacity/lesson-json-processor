import re
import pandas as pd
from glob import glob
import sys
import os
import json
import csv
import re

def create_issue_tracker_dict(data, nd, ver, lesson):
    '''
    Create an issue tracker for the lesson

    INPUT
    data - holds the json loader to traverse the json
    nd, ver, lesson  - values from the json or filename to create the URL

    RETURN
    issue_tracker - dictionary with a key of the mocha URL and value of a
                       list with 1 iterm being the concept/page name
    '''
    issue_tracker = {}
    count = 0
    for pages in data['concepts']:
        if count < len(data['concepts']):
            page = pages['key'] # pages/concept key
            url = '{}/{}/{}/{}'.format(nd, ver, lesson, page)
            issue_tracker[url] = [data['concepts'][count]['title']] # add page title to list as values in dictionary
            count += 1 # increment the count to go to next page
    return issue_tracker

# Atom Checks

############### Chencai Programming Question Check ###############
def programming_question_check(it, url, core):
    if core['question']['semantic_type'] == "ProgrammingQuestion":
          it[url].append(["Programming Question"])
    elif core['question']['semantic_type'] == "ImageFormQuestion":
          it[url].append(["Image Form Question"])
############### Chencai Programming Question Check ###############

############### Chencai Workspace Check ###############
def workspace_check(it, url, core):
    if core['semantic_type'] == "WorkspaceAtom":
          if core['pool_id'] == "jupyter":
                it[url].append([core['pool_id'],core['name'],core['configuration']['blueprint']['conf']['defaultPath']])
          elif core['pool_id'] == "sqlwidget":
                it[url].append([core['pool_id'],core['name']," "])
          else:
                it[url].append([core['pool_id']," "," "])
############### Chencai Workspace Check ###############

# Customize Your Checks
def initialize_checks(issue_tracker, nd, ver, lesson, data):
    '''Does the initial check of the atom type and then will initiate the appropriate check.'''
    it = issue_tracker
    url = '{}/{}/{}/'.format(nd, ver, lesson)
    for concept_num in range(0, len(data['concepts'])): # Every Concept (N)
        url_key = url  + data['concepts'][concept_num]['key']
        for atom_num in range(0, len(data['concepts'][concept_num]['atoms'])): # Every Atom (M)
            core = data['concepts'][concept_num]['atoms'][atom_num]
            atom_type = core['__typename']

############### Chencai Programming Question Check ###############
            if "QuizAtom" == atom_type:
                programming_question_check(it, url_key, core)
############### Chencai Programming Question Check ###############

############### Chencai Workspace Check ###############
            # if atom_type == "WorkspaceAtom":
            #     workspace_check(it, url_key, core)
############### Chencai Workspace Check ###############

    return it

# Finalize and Create the CSV for Output
def clean_and_lesson_name(issue_tracker, lesson_name):
    '''This will clean the dictionary to only pages with issues and if there are issues will add the lesson title'''
    for key in list(issue_tracker):
        if len(issue_tracker[key]) == 1:
            del issue_tracker[key]
        else:
            issue_tracker[key].insert(0, lesson_name)
    return issue_tracker

def create_csv(issue_tracker, nd):
    '''
    Creates a csv called 'issue_tracker.csv' from a dictionary 'issue_tracker'

    INPUT - comprehensive dictionary of all issues for the JSONs in the folder.

    OUTPUT - a CSV organized as follows
        Column Titles:
         - Lesson Name - from JSON
         - Page Name - from JSOn
         - URL - goes to Mocha
         - Issue - contain 1 issue in a given row
    '''
    with open('issue_tracker.csv', 'w') as csv_file:
        headers = ['Course Key', 'Lesson Name', 'Page Name', 'Issue'] # Labels
        writer = csv.DictWriter(csv_file, fieldnames = headers)
        writer.writeheader()
        for key,value in issue_tracker.items():
            for items in range (2, len(value)):
                writer.writerow({'Course Key': nd, 'Lesson Name': value[0], 'Page Name': value[1], 'Issue': value[items][0]})
    print("Your course has been checked and your csv file is in the main directory.")

def main():
    course_dict = {}
    for filename in os.listdir("jsons"):
        #iterates through each json file
        if filename.endswith('.json'):
            # print(filename)
            file =  open("jsons/" + filename)
            data = json.load(file)

            # initialize static lesson values
            lesson = data['key'] #lesson key
            nd = filename.split('_')[0] # nd key from filename
            ver = filename.split('_')[2] # version from filename (this can't be found when exporting json from mocha/coco)

            # creates, checks, and organizes them into 1 dictionary
            issue_tracker = create_issue_tracker_dict(data, nd, ver, lesson)
            checked = initialize_checks(issue_tracker, nd, ver, lesson, data)
            lesson_dict = clean_and_lesson_name(checked, data['title'])
            course_dict.update(lesson_dict)
            file.close()

    # uses the dictionary to create a csv
    create_csv(course_dict, nd)

# Enter Values

main()
