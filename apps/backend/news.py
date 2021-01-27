import os
import json
import string
import random
from werkzeug.utils import secure_filename
from config import PATH_NEWS, ALLOWED_EXTENSIONS, UPLOAD_PATH, PATH_IMAGES

def delete_news(news_id):
    obj_news = ""

    # Read
    with open(PATH_NEWS  + news_id + ".json", "r") as file_news:
        data_news = file_news.read()
        obj_news = json.loads(data_news)

    # Remove thumbnail
    if os.path.exists(obj_news["thumbnail"]):
        os.remove(obj_news["thumbnail"])

    # Remove news
    if os.path.exists(PATH_NEWS + news_id + ".json"):
        os.remove(PATH_NEWS + news_id + ".json")

def create_news(new_content, upload_file = None):
    obj_news = ""
    news_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

    # Write news 
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + filename

        # Save to upload folder
        upload_file.save(os.path.join(UPLOAD_PATH, filename))

        # Move new file from upload folder
        os.replace(UPLOAD_PATH + "/" + filename, PATH_IMAGES + "latestNews/" + filename)

        # Update image path in news file
        new_content = new_content.to_dict() 
        new_content["thumbnail"] = PATH_IMAGES + "latestNews/" + filename
        new_content["id"] = news_id

    # Write
    with open(PATH_NEWS + news_id + ".json", "w") as file_news:
        file_news.write(json.dumps(new_content))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
