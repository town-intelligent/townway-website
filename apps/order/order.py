import os
import json
from config import PATH_ORDER

def convert_cart_cookie(str_order):
    response = ""
    list_order = []

    if str_order == None:
        return ""

    try:
        list_order = json.loads(str_order)
    except Exception as e:
        return e

    for obj in list_order:
        response = response + "規格:" + obj["spec"] + ", " + "名稱:" + obj["name"] + ", " + "數量:" + str(obj["count"]) + ", " + "價格:" + str(obj["cost"]) + "; "

    return response

def delete_order(order_id):
    os.remove(PATH_ORDER + order_id + ".json")

def list_order():
    list_order = []
    list_order_files = os.listdir(PATH_ORDER)

    for obj in list_order_files:
        with open(PATH_ORDER + obj , "r") as outfile:
            obj_order = json.load(outfile)
            list_order.append(obj_order)

    return list_order

def save_order(request_data):
    with open(PATH_ORDER + request_data["id"] + ".json", "w") as outfile:
        json.dump(request_data, outfile)

def get_order(id_order):
    with open(PATH_ORDER + id_order + ".json", "r") as outfile:
        obj_message = json.load(outfile)

        message = ""
        message = message + "- 訂單編號: " + obj_message["id"] + "<br>"
        message = message + "- 訂購人姓名: " + obj_message["name_order"] + "<br>"
        message = message + "- 訂購人手機: " + obj_message["order_cellphone"] + "<br>"
        message = message + "- 訂購人電話: " + obj_message["order-phone"] + "<br>"
        message = message + "- 訂購人地址: " + obj_message["order_address"] + "<br>"
        message = message + "- 訂購人 email: " + obj_message["email_order"] + "<br>"
        message = message + "- 收件人姓名: " + obj_message["recipient_name"] + "<br>"
        message = message + "- 收件人手機: " + obj_message["recipient_cellphone"] + "<br>"
        message = message + "- 收件人電話: " + obj_message["recipient_phone"] + "<br>"
        message = message + "- 收件人地址: " + obj_message["recipient_address"] + "<br>"
        message = message + "- 收件人 email: " + obj_message["recipient_email"] + "<br>"
        message = message + "- 付款方式: " + obj_message["method"] + "<br>"
        message = message + "- 發票: " + obj_message["invoice"] + "<br>"
        message = message + "- 需求: " + obj_message["comment"] + "<br>"
        message = message + "- 商品: " + obj_message["order"] + "<br>"

        return message
