# Mocha Lesson JSON Processor

## Identify Deprecated quizzes `find_deprecated.py`

This script identifies all deprecated quiz types in YAML and/or JSON lesson files downloaded from Mocha and outputs the findings to a CSV file.

### Output

-   Course Key
-   Lesson Name
-   Page Name
-   Issue
-   Quiz ID

## Identify Matching quizzes `find_matching.py`

This script identifies all matching quizzes in YAML and/or JSON lesson files downloaded from Mocha and outputs the findings to a CSV file.

### Output

-   Course Key
-   Lesson Name
-   Page Name
-   Issue

## Instructions

1. Download lesson JSON and/or YAML files from Mocha
2. Save JSONS in the `/jsons` folder
3. Save YAML files in the `/yamls` folder
4. Run the python code:

    ```py
    python3 find_deprecated.py
    ```

    OR

    ```py
    python3 find_matching.py
    ```

5. Download `issue_tracker.csv`.
6. [OPTIONAL] Delete the JSON and YAML files
    ```py
    python3 delete_files.py
    ```
