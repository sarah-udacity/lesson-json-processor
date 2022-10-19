import pandas as pd
from glob import glob
import os
import json
import csv

def create_issue_tracker_dict(data):
    '''
    Create an issue tracker for the lesson

    INPUT
    data - holds the json loader to traverse the json

    RETURN
    issue_tracker - dictionary to hold results
    '''
    issue_tracker = {}
    count = 0
    for pages in data['concepts']:
        if count < len(data['concepts']):
            item_key = pages['key'] # pages/concept key
            issue_tracker[item_key] = [data['concepts'][count]['title']] # add page title to list as values in dictionary
            count += 1 # increment the count to go to next page
    return issue_tracker

# Check for deprecated quizzes
def deprecated_atom_check(it, item_key, core):
    if core['question']['semantic_type'] == "ProgrammingQuestion":
          it[item_key].append("Programming Question")
    elif core['question']['semantic_type'] == "ImageFormQuestion":
          it[item_key].append("Image Form Question")
    elif core['question']['semantic_type'] == "CodeGradedQuestion":
          it[item_key].append("Code Graded Question")
    elif core['question']['semantic_type'] == "QuestionInterface":
        it[item_key].append("Question Interface")
    elif core['question']['semantic_type'] == "IFrameQuestion":
        it[item_key].append("IFrame Question")


# Customize Your Checks
def initialize_checks(issue_tracker, cdkey, ver, lesson, data):
    '''Checks atom type and initiates check for deprecated quiz types.'''
    for concept_num in range(0, len(data['concepts'])): # Every Concept (N)
        item_key = data['concepts'][concept_num]['key']
        for atom_num in range(0, len(data['concepts'][concept_num]['atoms'])): # Every Atom (M)
            core = data['concepts'][concept_num]['atoms'][atom_num]
            atom_type = core['__typename']

            if "QuizAtom" == atom_type:
                deprecated_atom_check(issue_tracker, item_key, core)
    return issue_tracker

# Create the CSV
def clean_and_lesson_name(issue_tracker, cdkey, lesson_name):
    '''This will clean the dictionary to include only pages with issues and if there are issues will add the lesson title'''
    for key in list(issue_tracker):
        if len(issue_tracker[key]) == 1:
            del issue_tracker[key]
        else:
            issue_tracker[key].insert(0, lesson_name)
            issue_tracker[key].insert(0, cdkey)
    return issue_tracker

def create_csv(issue_tracker):
    '''
    Creates a csv called 'issue_tracker.csv' from a dictionary 'issue_tracker'

    INPUT - comprehensive dictionary of all issues for the JSONs in the folder.

    OUTPUT - a CSV organized as follows
        Column Titles:
         - Course Key (cdkey or part key)
         - Lesson Name
         - Page Name
         - Issue
    '''
    with open('issue_tracker.csv', 'w') as csv_file:
        headers = ['Course Key', 'Lesson Name', 'Page Name', 'Issue'] # Labels
        writer = csv.DictWriter(csv_file, fieldnames = headers)
        writer.writeheader()
        for key,value in issue_tracker.items():
            writer.writerow({'Course Key': value[0], 'Lesson Name': value[1], 'Page Name': value[2], 'Issue': value[3]})
    print("Your course has been checked and your csv file is in the main directory.")

def main():
    course_dict = {}
    for filename in os.listdir("jsons"):

        # iterates through each json file
        if filename.endswith('.json'):
            file =  open("jsons/" + filename)
            data = json.load(file)

            # initialize static lesson values
            lesson = data['key'] #lesson key
            cdkey = filename.split('_')[0] # cdkey key from filename
            ver = filename.split('_')[2] # version from filename (this can't be found when exporting json from mocha/coco)

            # creates, checks, and organizes them into 1 dictionary
            issue_tracker = create_issue_tracker_dict(data)
            checked = initialize_checks(issue_tracker, cdkey, ver, lesson, data)
            lesson_dict = clean_and_lesson_name(checked, cdkey, data['title'])
            course_dict.update(lesson_dict)
            file.close()

    # uses the dictionary to create a csv
    create_csv(course_dict)

# Enter Values

main()
