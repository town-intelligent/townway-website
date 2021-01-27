import os
import math
import json
from os import listdir
from apps.projects.config import PROJECT_NUMBERS_OF_ONE_PAGE, PATH_PROJECTS_LIST

def load_project_info(name):
    file_projects = open( str(os.path.dirname(os.path.abspath(__file__))) + "/../../" + PATH_PROJECTS_LIST, "r")
    list_projects = file_projects.readlines()

    for obj in list_projects:
        obj_project = json.loads(obj)
        if name == obj_project["name"]:
            return obj_project

def load_projects(name, page):
    list_object = []

    obj_project_info = load_project_info(name)
    list_projects = listdir(str(os.path.dirname(os.path.abspath(__file__))) + "/../../" + obj_project_info["path"])

    for filename in list_projects:
        with open(str(os.path.dirname(os.path.abspath(__file__))) + "/../../" + obj_project_info["path"] + filename, "r") as file_project:
            data_project = file_project.read()
            list_object.append(json.loads(data_project))

    # filter sub-list by page
    list_object = list_object[(PROJECT_NUMBERS_OF_ONE_PAGE*page) - PROJECT_NUMBERS_OF_ONE_PAGE:PROJECT_NUMBERS_OF_ONE_PAGE*page]
    
    return list_object

def cal_project_pages(name):
    obj_project_info = load_project_info(name)
    list_projects = listdir(str(os.path.dirname(os.path.abspath(__file__))) + "/../../" + obj_project_info["path"])

    total_pages = math.ceil(len(list_projects)/PROJECT_NUMBERS_OF_ONE_PAGE)

    return total_pages
