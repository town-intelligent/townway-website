import os
import math
import json
from os import listdir
from apps.news.config import NEWS_NUMBERS_OF_ONE_PAGE, PATH_NEWS

def load_news(page):
    list_object = []
    list_news = listdir(str(os.path.dirname(os.path.abspath(__file__))) + "/../../" + PATH_NEWS)

    for filename in list_news:
        with open(str(os.path.dirname(os.path.abspath(__file__))) + "/../../" + PATH_NEWS + filename, "r") as file_news:
            data_news = file_news.read()
            list_object.append(json.loads(data_news))

    # filter sub-list by page
    list_object = list_object[(NEWS_NUMBERS_OF_ONE_PAGE*page) - NEWS_NUMBERS_OF_ONE_PAGE:NEWS_NUMBERS_OF_ONE_PAGE*page]

    return list_object

def cal_news_pages():
    list_news = listdir(str(os.path.dirname(os.path.abspath(__file__))) + "/../../" + PATH_NEWS)

    total_pages = math.ceil(len(list_news)/NEWS_NUMBERS_OF_ONE_PAGE)

    return total_pages
