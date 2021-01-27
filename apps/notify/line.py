import json
import sys
from linebot import LineBotApi
from linebot.models import TextSendMessage
from config import CHANNEL_ACCESS_TOKEN, TYPE_SHOPPING_CART, \
    TYPE_GOODIDEA, TYPE_CONTACT_US, TYPE_ORGANICCROPS

def format_organiccrops(obj_message):
    message = "Hello! 您有新的冬筍會員:" + "\n"
    message = message + "- 姓名: " + obj_message["name"] + "\n"
    message = message + "- email: " + obj_message["email"] + "\n"
    message = message + "- 手機: " + obj_message["cellphone"] + "\n"
    message = message + "- 電話: " + obj_message["phone"] + "\n"
    message = message + "- LINE: " + obj_message["line"] + "\n"
    message = message + "- 地址: " + obj_message["address_receiver"] + "\n"
    message = message + "- 領取方式: " + obj_message["get_method"] + "\n"
    
    return message

def format_contact_us(obj_message):
    message = "Hello! 您有新的好意見:" + "\n"
    message = message + "- 姓名: " + obj_message["name"] + "\n"
    message = message + "- email: " + obj_message["email"] + "\n"
    message = message + "- 手機: " + obj_message["cellphone"] + "\n"
    message = message + "- 電話: " + obj_message["phone"] + "\n"
    message = message + "- 意見: " + obj_message["comment"] + "\n"
 
    return message

def format_good_idea(obj_message):
    message = "Hello! 您有新的好點子夥伴:" + "\n"
    message = message + "- 姓名: " + obj_message["name"] + "\n"
    message = message + "- 手機: " + obj_message["cellphone"] + "\n"
    message = message + "- 電話: " + obj_message["phone"] + "\n"
    message = message + "- email: " + obj_message["email"] + "\n"
    message = message + "- 專案: " + obj_message["project"] + "\n"
    message = message + "- 專業領域: " + obj_message["skill"] + "\n"
    message = message + "- 備註: " + obj_message["comment"] + "\n"

    return message

def format_shop_cart(obj_message):
    message = "Hello! 您有新的購物車訂單:" + "\n"
    message = message + "- 訂單編號: " + obj_message["id"] + "\n"
    message = message + "- 訂購人姓名: " + obj_message["name_order"] + "\n"
    message = message + "- 訂購人手機: " + obj_message["order_cellphone"] + "\n"
    message = message + "- 訂購人電話: " + obj_message["order-phone"] + "\n"
    message = message + "- 訂購人地址: " + obj_message["order_address"] + "\n"
    message = message + "- 訂購人 email: " + obj_message["email_order"] + "\n"
    message = message + "- 收件人姓名: " + obj_message["recipient_name"] + "\n"
    message = message + "- 收件人手機: " + obj_message["recipient_cellphone"] + "\n"
    message = message + "- 收件人電話: " + obj_message["recipient_phone"] + "\n"
    message = message + "- 收件人地址: " + obj_message["recipient_address"] + "\n"
    message = message + "- 收件人 email: " + obj_message["recipient_email"] + "\n"
    message = message + "- 付款方式: " + obj_message["method"] + "\n"
    message = message + "- 發票: " + obj_message["invoice"] + "\n"
    message = message + "- 需求: " + obj_message["comment"] + "\n"
    message = message + "- 商品: " + obj_message["order"] + "\n"

    return message

def broadcat(obj_message):
    message = "empty"

    try:
        if "type" in obj_message:
            if obj_message["type"] == TYPE_SHOPPING_CART:
                message = format_shop_cart(obj_message)
            elif obj_message["type"] == TYPE_GOODIDEA:
                message = format_good_idea(obj_message)
            elif obj_message["type"] == TYPE_CONTACT_US:
                message = format_contact_us(obj_message)
            elif obj_message["type"] == TYPE_ORGANICCROPS:
                message = format_organiccrops(obj_message)

    except Exception as e:
        print(e)        

    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text = message))
