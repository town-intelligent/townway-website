import string
import random
import json
from os import listdir
from flask import Flask, render_template, request, make_response, redirect
from apps.cart import CART_INFO, cal_veg_cost, cal_animal_light_cost, cal_bag_cost, cal_bird_cost
from apps.notify.line import broadcat as line_broadcat
from apps.projects.document import load_projects, cal_project_pages
from apps.news.document import cal_news_pages, load_news
from apps.backend.project import create_project, update_project, delete_project
from apps.backend.news import create_news, delete_news
from apps.order.order import save_order, get_order, list_order, delete_order, convert_cart_cookie
from config import PATH_GOOD_IDEAS, UPLOAD_PATH, ALLOWED_EXTENSIONS, \
    TYPE_SHOPPING_CART, TYPE_GOODIDEA, TYPE_CONTACT_US, TYPE_ORGANICCROPS

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aboutUs")
def aboutUs():
    name = request.args.get("name")

    if name == "aboutBeYoungGarden":
        return render_template("aboutBeYoungGarden.html")
    elif name == "aboutIceRoom":
        return render_template("aboutIceRoom.html")
    elif name == "aboutSkyYard":
        return render_template("aboutSkyYard.html")
    elif name == "aboutDigitalTownee":
        return render_template("aboutDigitalTownee.html")
    elif name == "aboutAsiaCreation":
        return render_template("aboutAsiaCreation.html")
    else:
        return render_template("aboutUs.html")

@app.route("/goodIdea", methods=["GET", "POST"])
def goodIdea():
    if request.method == "POST":
        request_data = ""
        # Check request well-form
        try:
            request_data = request.form
        except:
            return {"status":"Error", "msg":"Failed to decode JSON object"}

        request_data = request_data.to_dict()
        request_data["type"] = TYPE_GOODIDEA
        line_broadcat(request_data)

    list_object = []
    name = request.args.get("name", "goodIdea")
    page = int(request.args.get("page", 1))

    total_pages = cal_project_pages(name)
    list_object = load_projects(name, page)

    return render_template(name + ".html", name = name, list_object = list_object, total_pages = total_pages, page = page)

@app.route("/goodIdeaForm")
def goodIdeaForm():
    return render_template("goodIdeaForm.html")

@app.route("/goodIdeaInfo")
def goodIdeaInfo():
    project_id = request.args.get("id")
    name = request.args.get("name")

    with open(app.root_path + PATH_GOOD_IDEAS + name + "/" + project_id + ".json", "r") as file_project:
        data_project = file_project.read()
        obj = json.loads(data_project)

        return render_template("goodIdeaInfo.html", obj = obj)

    return ""

@app.route("/store")
def store():
    return render_template("store.html")

@app.route("/storeProductInfo")
def storeProductInfo():
    store_id = int(request.args.get("id", 1))
    if store_id == 1:
        return render_template("storeProductInfo.html")
    elif store_id == 2:
        return render_template("storeProductInfo_02.html")
    elif store_id == 3:
        return render_template("storeProductInfo_03.html")
    elif store_id == 4:
        return render_template("storeProductInfo_04.html")
    elif store_id == 5:
        return render_template("storeProductInfo_05.html")
    elif store_id == 6:
        return render_template("storeProductInfo_06.html")
    elif store_id == 7:
        return render_template("storeProductInfo_07.html")
    elif store_id == 8:
        return render_template("storeProductInfo_08.html")

@app.route("/storeProductInfo_02")
def storeProductInfo_02():
    return render_template("storeProductInfo_02.html")

@app.route("/latestNews")
def latestNews():

    list_news = []
    page = int(request.args.get("page", 1))

    total_pages = cal_news_pages()
    list_object = load_news(page)

    return render_template("latestNews.html", list_object = list_object, total_pages = total_pages, page = page)

@app.route("/contactUs", methods=["GET", "POST"])
def contactUs():
    if request.method == "POST":
        request_data = ""
        # Check request well-form
        try:
            request_data = request.form
        except:
            return {"status":"Error", "msg":"Failed to decode JSON object"}

        # Line bot
        request_data = request_data.to_dict()
        request_data["type"] = TYPE_CONTACT_US
        line_broadcat(request_data)

    return render_template("contactUs.html")

# Smart shop module - start
@app.route("/organicCrops", methods=["GET", "POST"])
def organicCrops():
    if request.method == "POST":
        request_data = ""
        order_name = ""
        # Check request well-form
        try:
            request_data = request.form
        except:
            return {"status":"Error", "msg":"Failed to decode JSON object"}

        # TODO
        request_data = request_data.to_dict()
        request_data["type"] = TYPE_ORGANICCROPS
        line_broadcat(request_data)

    page = request.args.get("page")

    if page == "organicCropsMembers":
        return render_template("organicCropsMembers.html")
    elif page == "organicCropsProduct":
        return render_template("organicCropsProduct.html")
    else:
        return render_template("organicCrops.html")

@app.route("/purchaseOrderCheck_01", methods=["GET", "POST"])
def purchaseOrderCheck_01():
    order_id = None
    if request.method == "POST":
        request_data = ""
        order_name = ""
        # Check request well-form
        try:
            request_data = request.form
        except:
            return {"status":"Error", "msg":"Failed to decode JSON object"}

        # Get cart
        str_order = convert_cart_cookie(request.cookies.get("list_order"))

        request_data = request_data.to_dict()

        # Save order
        order_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        request_data["id"] = order_id
        request_data["order"] = str_order

        save_order(request_data)

        # Line Bot
        request_data["type"] = TYPE_SHOPPING_CART
        line_broadcat(request_data)

    return render_template("purchaseOrderCheck_01.html", order_id = order_id)

# Callback function of add to cart
@app.route('/add_cart', methods=["POST"])
def add_cart():
    request_data = ""
    order_name = ""

    print("Hello request.form = " + str(request.form))
    # Check request well-form
    try:
        request_data = request.form
    except:
        return {"status":"Error", "msg":"Failed to decode JSON object"}

    # TODO: Need refactor
    if request_data["name"] == "veg_box":
        order_name = "蔬菜箱"
        cost = cal_veg_cost(request_data["spec"], request_data["count"])
    elif request_data["name"] == "animal":
        order_name = "動物燈飾"
        cost = cal_animal_light_cost(request_data["count"])
    elif request_data["name"] == "bag":
        order_name = "銀髮竹編ＤＩＹ包"
        cost = cal_bag_cost(request_data["spec"], request_data["count"])
    elif request_data["name"] == "bird":
        order_name = "平衡鳥"
        cost = cal_bird_cost(request_data["spec"], request_data["count"])

    # Add to cookie
    list_order = []
    str_order = request.cookies.get("list_order")

    if str_order != None:
        list_order = json.loads(str_order)

    response = make_response(json.dumps({'success':True}), 200, {'ContentType':'application/json'})
    obj_order = CART_INFO 
    try:
        obj_order["name"] = order_name
        obj_order["spec"] = request_data["spec"]
        obj_order["count"] = request_data["count"]
        obj_order["cost"] = str(cost)
        obj_order["comment"] = request_data["comment"]
    except Exception as e:
        pass

    list_order.append(obj_order)
    response.set_cookie("list_order", json.dumps(list_order), max_age = 3600)

    return response

# bill page
@app.route("/purchase_01")
def purchase_01():
    list_order = []
   
    try:
        str_order = request.cookies.get("list_order")
        list_order = json.loads(str_order)
    except Exception as e:
        pass

    # return json.dumps(list_order)
    return render_template("purchase_01.html", list_order = list_order)

# final submit
@app.route("/purchase_02")
def purchase_02():
    list_order = []

    try:
        str_order = request.cookies.get("list_order")
        list_order = json.loads(str_order)
    except Exception as e:
        pass

    total_cost = 0
    for obj in list_order:
        total_cost = int(obj["cost"]) + total_cost

    return render_template("purchase_02.html", list_order = list_order, total_cost = total_cost)

@app.route('/search_order', methods=["POST"])
def search_order():
    request_data = ""
    # Check request well-form
    try:
        request_data = request.form
    except:
        return {"status":"Error", "msg":"Failed to decode JSON object"}

    content = get_order(request_data["id_order"])

    return render_template("order_info.html", content = content)

@app.route('/get_cart')
def get_cart():
    response = ""
    list_order = []
    str_order = request.cookies.get("list_order")

    if str_order == None:
        return ""

    try:
        list_order = json.loads(str_order)
    except Exception as e:
        return e

    return json.dumps(list_order)

@app.route('/del_cart')
def del_cart():
    del_id = request.args.get("id")

    # response = make_response(json.dumps({'success':True}), 200, {'ContentType':'application/json'})
    response = make_response(redirect("/purchase_01"))
    list_order = []

    if del_id == None:
        response.delete_cookie("list_order")
    else:
        list_order = json.loads(request.cookies.get("list_order"))
        list_order.remove(list_order[int(del_id)])
        response.set_cookie("list_order", json.dumps(list_order), max_age = 3600)

    return response

# Smart shop module - end

## Admin page - start

@app.route('/backend')
def backend():
    list_object = []
    total_pages = 1
    name = request.args.get("name")
    page = int(request.args.get("page", 1))

    if name == None:
        return render_template("backend/backend.html")

    if "goodIdea" in name:
        total_pages = cal_project_pages(name)
        list_object = load_projects(name, page)
    elif "latestNews" == name:
        total_pages = cal_news_pages()
        list_object = load_news(page)
    elif "order" == name:
        if request.args.get("command") == "delete":
            delete_order(request.args.get("id"))
        elif request.args.get("command") == "view":
            content = get_order(request.args.get("id"))
            return render_template("order_info.html", content = content)


        list_orders = list_order()
        return render_template("backend/order.html", list_orders = list_orders)

    return render_template("backend/" + name + ".html",  \
        name = name, list_object = list_object, \
        total_pages = total_pages, page = page)

@app.route("/backend_goodIdeaInfo", methods=["GET", "POST"])
def backend_goodIdeaInfo():
    project_id = ""
    name = ""
    image_path = ""

    if request.method == "GET":
        project_id = request.args.get("id")
        name = request.args.get("name")

        # Create project page
        if request.args.get("command") == "new":
            return render_template("backend/create_goodIdeaInfo.html", name = name, command = "new")
        elif request.args.get("command") == "delete":
            delete_project(name, project_id)
            return redirect("/backend?name=" + name)

    if request.method == "POST":
        request_data = ""
        # Check request well-form
        try:
            request_data = request.form
        except:
            return {"status":"Error", "msg":"Failed to decode JSON object"}

        project_id = request_data.get("id")
        name = request_data.get("name")

        # New project
        if request_data.get("command") == "new":
            create_project(name, request_data, request.files["file"])

            return redirect("/backend?name=" + name)

        # Update project files
        try:
            update_project(name, project_id, request_data, request.files["file"])
        except:
            return {"status":"Error", "msg":"Update project file fail."}

    with open(PATH_GOOD_IDEAS + name + "/" + project_id + ".json", "r") as file_project:
        data_project = file_project.read()
        obj = json.loads(data_project)

        return render_template("backend/goodIdeaInfo.html", obj = obj, name = name)

    return ""

@app.route("/backend_latestNews", methods=["GET", "POST"])
def backend_latestNews():
    news_id = ""
    image_path = ""

    if request.method == "GET":
        news_id = request.args.get("id")

        # Create news page
        if request.args.get("command") == "new":
            return render_template("backend/create_latestNews.html", command = "new")
        elif request.args.get("command") == "delete":
            delete_news(news_id)
            return redirect("/backend?name=latestNews")

    if request.method == "POST":
        request_data = ""
        # Check request well-form
        try:
            request_data = request.form
        except:
            return {"status":"Error", "msg":"Failed to decode JSON object"}

        news_id = request_data.get("id")

        # New one news
        if request_data.get("command") == "new":
            create_news(request_data, request.files["file"])
            return redirect("/backend?name=latestNews")

## Admin page - end

if __name__ == '__main__':
    app.run(debug = True, threaded = True, host = "0.0.0.0", port = 5004)
