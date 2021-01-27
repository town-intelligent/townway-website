CART_INFO = {"thumbnail":"", "name":"", "spec":"", "count":0, "cost":0, "comment":""}

def cal_veg_cost(spec, count):
    cost = 0
    if spec == "60":
        cost = 300
    elif spec == "90":
        cost = 400
    elif spec == "120":
        cost = 500
    else:
        cost = 0

    return cost*int(count)

def cal_animal_light_cost(count):
    return int(count) * 2600

def cal_bag_cost(spec, count):
    cost = 0
    if spec == "銀髮竹編ＤＩＹ包（大）":
        cost = 880
    else:
        cost = 770

    return cost*int(count)

def cal_bird_cost(spec, count):
    cost = 4800

    return cost*int(count)
