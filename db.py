import pymongo
import os
import uuid

client = pymongo.MongoClient(os.environ["MONGO"])
db = client.main


# event = {
#     "id":"some-hash-uuid",
#     "title":"Event Title",
#     "image":"image-link",
#     "desc":"description",
#     "register":"open/closed"
#     "timestamp":""
#     "group":"0/1 individual/ 2+ group"
#     "fee":{
#         "ieee":50,
#         "non":100,
#         "cs":10
#     }
# }


def get_events():
    events = []
    for e in db.events.find():
        e.pop("_id")
        events.append(e)
    return events

def get_event(id):
    event = db.events.find_one({"id":id})
    event.pop("_id")
    return event

def add_event(event_dict):
    e_id = uuid.uuid4().hex
    event_dict["id"] = e_id
    db.events.insert_one(event_dict)
    return e_id

def delete_event(id):
    db.events.delete_one({"id":id})

def update_event(event_dict):
    id = event_dict["id"]
    db.events.find_one_and_replace({"id":id},event_dict)



# reg = {
#     "id"
#     "event_id"
#     "timestamp"
#     "status"
#     "email"
#     "amount"
#     "members":[]
# }

# status = registered
def add_reg(reg_info):
    reg_id = uuid.uuid4().hex
    reg_info["id"] = reg_id
    reg_info["status"] = "registered"
    db.regs.insert_one(reg_info)
    return reg_id

def delete_reg(reg_id):
    db.regs.delete_one({"id":reg_id})

def get_reg(reg_id):
    reg = db.regs.find_one({"id":reg_id})
    reg.pop("_id")
    return reg


# update reg functions
# status = paid
def mark_paid(reg_id):
    reg = get_reg(reg_id)
    reg["status"] = "paid"
    db.regs.find_one_and_replace({"id":reg_id},reg)

# status = attended
def mark_attended(reg_id):
    reg = get_reg(reg_id)
    reg["status"] = "attended"
    db.regs.find_one_and_replace({"id":reg_id},reg)




# status = registered, paid, attended
def get_regs(event_id, status="any"):
    regs_list = []
    if status=="any":
        regs = db.regs.find({"event_id":event_id})
    else:
        regs = db.regs.find({"event_id":event_id,"status":status})

    for r in regs:
        r.pop("_id")
        regs_list.append(r)

    return regs_list



# group and individual
# def get_member_regs(email):
#     regs_list = []
#     regs = db.regs.find({"email":email})

#     for r in regs:
#         r.pop("_id")
#         regs_list.append(r)

#     return regs_list