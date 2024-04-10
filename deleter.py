import os 

def get_project_path():
    # Get the directory of the current Python script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the directory of the project (one level up from the current directory)
    project_dir = os.path.dirname(current_dir)
    return project_dir

upload_dir = os.path.join(get_project_path(), 'upload_raggen')


