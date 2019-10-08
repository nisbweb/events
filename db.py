import pymongo
import os
import uuid
import datetime

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


#                                m
#   mmm   m   m   mmm   m mm   mm#mm   mmm
#  #"  #  "m m"  #"  #  #"  #    #    #   "
#  #""""   #m#   #""""  #   #    #     """m
#  "#mm"    #    "#mm"  #   #    "mm  "mmm"


def get_events(after=None):
    events = []
    query = {}
    if after:
        after_time = datetime.datetime.strptime(
            after, '%d/%m/%Y %H:%M:%S')
        query["timestamp"] = {
            "$gte": after_time
        }
    for e in db.events.find(query):
        e.pop("_id")
        events.append(e)
    return events


def get_event(id):
    event = db.events.find_one({"id": id})
    event.pop("_id")
    return event


def add_event(event_dict):
    e_id = uuid.uuid4().hex
    event_dict["id"] = e_id
    event_dict["timestamp"] = datetime.datetime.strptime(
        event_dict["timestamp"], '%d/%m/%Y %H:%M:%S')
    db.events.insert_one(event_dict)
    return e_id


def delete_event(id):
    db.events.delete_one({"id": id})


def update_event(event_dict):
    id = event_dict["id"]
    db.events.find_one_and_replace({"id": id}, event_dict)


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
    reg_info["timestamp"] = datetime.datetime.today()
    if db.regs.insert_one(reg_info):
        return reg_id
    else:
        return None


def delete_reg(reg_id):
    return db.regs.delete_one({"id": reg_id})


def get_reg(reg_id):
    reg = db.regs.find_one({"id": reg_id})
    if reg:
        reg.pop("_id")
        return reg
    else:
        return None


# update reg functions
# status = paid
def update_reg_status(reg_id, status="registered"):
    reg = get_reg(reg_id)
    if reg:
        reg["status"] = status
        if db.regs.find_one_and_replace({"id": reg_id}, reg):
            return True

    return False


# status = registered, paid, attended
def get_regs(event_id, status="any"):
    regs_list = []
    if status == "any":
        regs = db.regs.find({"event_id": event_id})
    else:
        regs = db.regs.find({"event_id": event_id, "status": status})

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


#                  m      "
#  m mm    mmm   mm#mm  mmm     mmm    mmm    mmm
#  #"  #  #" "#    #      #    #"  "  #"  #  #   "
#  #   #  #   #    #      #    #      #""""   """m
#  #   #  "#m#"    "mm  mm#mm  "#mm"  "#mm"  "mmm"


# sample notice
# {
#     "id":"",
#     "topic":"general",
#     "message":"some message",
#     "data":{},
#     "timestamp":""
# }


def get_notices(after=None):
    query = {}
    notices = []
    if after:
        after_time = datetime.datetime.strptime(
            after, '%d/%m/%Y %H:%M:%S')
        query["timestamp"] = {
            "$gte": after_time
        }
    for e in db.notices.find(query):
        e.pop("_id")
        notices.append(e)
    return notices


def get_notice(id):
    notice = db.notices.find_one({"id": id})
    notice.pop("_id")
    return notice


def add_notice(notice_dict):
    n_id = uuid.uuid4().hex
    notice_dict["id"] = n_id
    notice_dict["timestamp"] = datetime.datetime.today()
    db.notices.insert_one(notice_dict)
    return n_id


def delete_notice(id):
    db.notices.delete_one({"id": id})


def update_notice(notice_dict):
    id = notice_dict["id"]
    db.notices.find_one_and_replace({"id": id}, notice_dict)
