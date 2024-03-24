import os
import json
import csv
import yaml

def convert_yamls():
    ''' Iterate through YAML files and return a JSON file with the same data'''
    for filename in os.listdir("yamls"):
        if filename.endswith('.yaml'):
            # open and load the YAML file
            yaml_file =  open("yamls/" + filename)
            loaded_yaml = yaml.safe_load(yaml_file)

            # create/open a JSON file with the same name
            json_file = open("jsons/" + os.path.splitext(filename)[0] + ".json", 'w')

            # convert the YAML contents to JSON
            json.dump(loaded_yaml, json_file)

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
          it[item_key].extend(["Programming Question", core['question']['evaluation_id']])
    elif core['question']['semantic_type'] == "ImageFormQuestion":
          it[item_key].extend(["Image Form Question", core['question']['evaluation_id']])
    elif core['question']['semantic_type'] == "CodeGradedQuestion":
          it[item_key].extend(["Code Graded Question", core['question']['evaluation_id']])
    elif core['question']['semantic_type'] == "QuestionInterface":
        it[item_key].extend(["Question Interface", core['question']['evaluation_id']])
    elif core['question']['semantic_type'] == "IFrameQuestion":
        it[item_key].extend(["IFrame question", core['question']['evaluation_id']])


# Intialize the check
def find_deprecated(issue_tracker, data):
    '''Check atom type and search for deprecated quiz types.'''
    for concept_num in range(0, len(data['concepts'])): # Every Concept (N)
        item_key = data['concepts'][concept_num]['key']
        for atom_num in range(0, len(data['concepts'][concept_num]['atoms'])): # Every Atom (M)
            core = data['concepts'][concept_num]['atoms'][atom_num]
            if '__typename' in core and core['__typename'] is not None:
                atom_type = core['__typename']

                if "QuizAtom" == atom_type:
                    deprecated_atom_check(issue_tracker, item_key, core)
    return issue_tracker

# Create the CSV
def clean_lesson_tracker(issue_tracker, cdkey, lesson_name):
    '''Clean the dictionary to include only pages with issues and add the lesson title'''
    for key in list(issue_tracker):
        if len(issue_tracker[key]) == 1:
            del issue_tracker[key]
        else:
            issue_tracker[key].insert(0, lesson_name)
            issue_tracker[key].insert(0, cdkey)
    return issue_tracker

def create_csv(issue_tracker):
    '''
    Create a csv called 'issue_tracker.csv' from a dictionary 'issue_tracker'

    INPUT - comprehensive dictionary of all issues for the JSONs in the folder.

    OUTPUT - a CSV organized as follows
        Column Titles:
         - Course Key (cdkey or part key)
         - Lesson Name
         - Page Name
         - Issue
         - Quiz ID
    '''
    with open('issue_tracker.csv', 'w') as csv_file:
        headers = ['Course Key', 'Lesson Name', 'Page Name', 'Issue', 'ID'] # Labels
        writer = csv.DictWriter(csv_file, fieldnames = headers)
        writer.writeheader()
        for key,value in issue_tracker.items():
            writer.writerow({'Course Key': value[0], 'Lesson Name': value[1], 'Page Name': value[2], 'Issue': value[3], 'ID': value[4]})
    print("Your course has been checked and your csv file is in the main directory.")

def main():
    course_dict = {}

    # convert YAML files to JSON
    convert_yamls()
    for filename in os.listdir("jsons"):

        # iterates through each json file
        if filename.endswith('.json'):
            file =  open("jsons/" + filename)
            lesson_data = json.load(file)

            # check if json has a concepts key
            if 'concepts' in lesson_data:
                 # get cdkey key from filename and lesson name from json
                cdkey = filename.split('_')[0]
                lesson_title = lesson_data['title']

                # create issue tracker for lesson
                lesson_issue_tracker = create_issue_tracker_dict(lesson_data)

                # check lesson json and return any deprecated quizzes
                found_issues = find_deprecated(lesson_issue_tracker, lesson_data)

                # clean up the found issues
                lesson_dict = clean_lesson_tracker(found_issues, cdkey, lesson_title)

                # add the cleaned issues to the course tracker and close the json file
                course_dict.update(lesson_dict)
                file.close()

    # uses the dictionary to create a csv
    create_csv(course_dict)

main()
