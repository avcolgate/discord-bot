import json
from money import *
from mainshop import *

# FUNC for buying smth in shop
async def buy_this(user,item_name):
    users = await get_users_data()

    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            type_= item["type"]
            if type_ != "background" and type_ != "nickname_color":
                person_ = item["person"]
            break

    # unkn name of item
    if name_ == None:
        return [False,1]


    bal = await update_bank(user)

    # having not enough money
    if bal[0]<price:
        return [False,2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["name"]
            if n == item_name:
                return [False,3]
            index+=1 
        if t == None:
            #if personality
            if type_ == "personality":
                obj = {"name":item_name, "type":type_, "person":person_}

            # if background or nickname_color
            elif type_ == "background" or type_ == "nickname_color":
                obj = {"name":item_name, "type":type_, "is_active" : 0}
                
            else:
                obj = {"name":item_name, "type":type_, "person":person_, "is_active" : 0}
            users[str(user.id)]["bag"].append(obj)
    except:
            # if personality
            if type_ == "personality":
                obj = {"name":item_name, "type":type_, "person":person_}

            # if background or nickname_color
            elif type_ == "background" or type_ == "nickname_color":
                obj = {"name":item_name, "type":type_, "is_active" : 0}

            else:
                obj = {"name":item_name, "type":type_, "person":person_, "is_active" : 0}
            users[str(user.id)]["bag"].append(obj)   

    with open("base.json","w") as f:
        json.dump(users,f)

    await update_bank(user,price*-1,"wallet")

    return [True,"Worked"]

# FUNC for selling smth in bag
async def sell_this(user,item_name,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                # 90% of price will return
                price = int(0.8* item["price"])
            break

    #unkn name of item
    if name_ == None:
        return [False,1]

    users = await get_users_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["name"]
            if n == item_name:
                del users[str(user.id)]["bag"][index]
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]  

    with open("base.json","w") as f:
        json.dump(users,f)

    await update_bank(user,price,"wallet")

    return [True,"Worked"]

async def active_command(user, item_name, is_active=0):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        type = item["type"].lower()
        if type != "background" and type != "nickname_color":
            person = item["person"].lower()
        else:
            person = '\0'
        if name == item_name:
            name_ = name
            type_ = type
            person_ = person
            break

    #unkn name of item
    if name_ == None:
        return [False,1]

    #print('found: ' + name_ + ' ' + type_ + ' ' + person_)

    users = await get_users_data()

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["name"]
            #print(n)
            n_type = thing["type"]
            #print(n_type)
            if n_type != "background" and n_type != "nickname_color":
                n_person = thing["person"]
            else:
                n_person = '\0'
            #print(n_person+'\n')
            if n == item_name:
                users[str(user.id)]["bag"][index]["is_active"] = 1
                t = 1
            elif n_type == type_ and n_person == person_:
                users[str(user.id)]["bag"][index]["is_active"] = 0
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]  

    with open("base.json","w") as f:
        json.dump(users,f)

    return [True,"Worked"]


async def deactivate_command(user, item_name, is_active=0):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        type = item["type"].lower()
        if name == item_name:
            name_ = name
            type_ = type
            break

    #unkn name of item
    if name_ == None:
        return [False,1]

    users = await get_users_data()

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["name"]
            n_type = thing["type"]
            if n == item_name:
                users[str(user.id)]["bag"][index]["is_active"] = 0
                t = 1
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]  

    with open("base.json","w") as f:
        json.dump(users,f)

    return [True,"Worked"]