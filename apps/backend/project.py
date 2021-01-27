import os
import json
import string
import random
from werkzeug.utils import secure_filename
from config import PATH_GOOD_IDEAS, ALLOWED_EXTENSIONS, UPLOAD_PATH, PATH_IMAGES

def delete_project(name, project_id):
    obj_project = ""

    # Read
    with open(PATH_GOOD_IDEAS  + name + "/" + project_id + ".json", "r") as file_project:
        data_project = file_project.read()
        obj_project = json.loads(data_project)
    
    # Remove thumbnail
    if os.path.exists(obj_project["thumbnail"]):
        os.remove(obj_project["thumbnail"])
 
    # Remove project
    if os.path.exists(PATH_GOOD_IDEAS  + name + "/" + project_id + ".json"):
        os.remove(PATH_GOOD_IDEAS  + name + "/" + project_id + ".json")

def create_project(name, new_content, upload_file = None):
    obj_project = ""
    project_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

    # Write project
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + filename

        # Save to upload folder
        upload_file.save(os.path.join(UPLOAD_PATH, filename))

        # Move new file from upload folder
        os.replace(UPLOAD_PATH + "/" + filename, PATH_IMAGES + name + "/" + filename)

        # Update image path in project file
        new_content = new_content.to_dict() 
        new_content["thumbnail"] = PATH_IMAGES + name + "/" + filename
        new_content["id"] = project_id

    # Write
    with open(PATH_GOOD_IDEAS  + name + "/" + project_id + ".json", "w") as file_project:
        file_project.write(json.dumps(new_content))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def update_project(name, project_id, new_content, upload_file = None):
    obj_project = ""

    # Read
    with open(PATH_GOOD_IDEAS  + name + "/" + project_id + ".json", "r") as file_project:
        data_project = file_project.read()
        obj_project = json.loads(data_project)
    
    # Update file
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + filename

        # Save to upload folder
        upload_file.save(os.path.join(UPLOAD_PATH, filename))

        # Remove old file
        if os.path.exists(new_content["thumbnail"][1:]):
            os.remove(new_content["thumbnail"][1:])

        # Move new file from upload folder
        os.replace(UPLOAD_PATH + "/" + filename, PATH_IMAGES + name + "/" + filename)

        # Update image path in project file
        new_content = new_content.to_dict() 
        new_content["thumbnail"] = PATH_IMAGES + name + "/" + filename

    # Write
    with open(PATH_GOOD_IDEAS  + name + "/" + project_id + ".json", "w") as file_project:
        file_project.write(json.dumps(new_content))
