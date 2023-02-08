import os

yamls = './yamls'
jsons = './jsons'

def delete_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Error: {e}')

delete_files(yamls)
delete_files(jsons)