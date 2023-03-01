# Mocha Lesson JSON Processor

## Identify Deprecated quizzes `find_deprecated.py`

This script identifies all deprecated quiz types in YAML and/or JSON lesson files downloaded from Mocha and outputs the findings to a CSV file.

### `find_deprecated.py` Output

- Course Key
- Lesson Name
- Page Name
- Issue
- Quiz ID

## Identify Matching quizzes `find_matching.py`

This script identifies all matching quizzes in YAML and/or JSON lesson files downloaded from Mocha and outputs the findings to a CSV file.

### `find_matching.py` Output

- Course Key
- Lesson Name
- Page Name
- Issue

## Identify YouTube IDs for all videos `find_video_yts.py`

This script identifies all the YouTube IDs for videos in JSON lesson files downloaded from Mocha and outputs the findings to a CSV file.

### `find_video_yts.py` Output

- Course Key
- Lesson Name
- Page Name
- YouTubeID

## Instructions

1. Download lesson JSON and/or YAML files from Mocha
2. Save JSONS in the `/jsons` folder
3. Run the python code:

    ```py
    python3 find_deprecated.py
    ```

    OR

    ```py
    python3 find_matching.py
    ```

    OR

    ```py
    python3 find_video_yts.py
    ```

5. Download `issue_tracker.csv`.
6. [OPTIONAL] Delete the JSON and YAML files

    ```py
    python3 delete_files.py
    ```
