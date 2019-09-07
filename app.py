from flask import Flask, request, jsonify
from db import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# Does nothing
@app.route('/')
def index():
    return jsonify({
        "status": "ok"
    })


@app.route("/events")
def events_controller():
    if "after" in request.args:
        events = get_events(after=request.args.get("after"))
        return jsonify(events)
    return jsonify(get_events())


@app.route("/event", methods=["GET", "PUT", "POST", "DELETE"])
def event_controller():
    if request.method == "GET":
        events = get_event(request.args.get("event_id"))
        return jsonify(events)

    elif request.method == "DELETE":
        delete_event(request.args.get("event_id"))
        return jsonify({"status": "ok"})

    elif request.method == "PUT":
        update_event(request.get_json())
        return jsonify({"status": "ok"})

    elif request.method == "POST":
        id = add_event(request.get_json())
        return jsonify({"status": "ok", "event_id": id})


@app.route("/regs")
def regs_controller():
    if "email" in request.args:
        return jsonify({
            "status": "error", 
            "error": "method not implemented yet."
            })

    elif "event_id" in request.args:
        if "status" in request.args:
            regs = get_regs(request.args.get("event_id"),
                            request.args.get("status"))
        else:
            regs = get_regs(request.args.get("event_id"))
        return jsonify(regs)


@app.route("/reg", methods=["GET", "POST", "PUT", "DELETE"])
def reg_controller():
    if request.method == "GET":
        reg = get_reg(request.args.get("reg_id"))
        if reg:
            return jsonify(reg)
        else:
            return jsonify({}), 204  # no content

    elif request.method == "DELETE":
        delete_reg(request.args.get("reg_id"))
        return jsonify({"status": "ok"})

    elif request.method == "POST":
        add_reg(request.get_json())
        return jsonify({"status": "ok"})

    elif request.method == "PUT":
        response_obj = request.get_json()
        if "status" in response_obj:  # registered, paid, attended
            reg_id = request.args.get("reg_id")
            o = update_reg_status(reg_id, response_obj["status"])
            if o:
                return jsonify(o)
            else:
                return jsonify({
                    "status": "error",
                    "error": "reg update operation failed"
                    })


@app.route("/notices")
def notices_controller():
    if "after" in request.args:
        notices = get_notices(after=request.args.get("after"))
        return jsonify(notices)
    return jsonify(get_notices())


@app.route("/notice", methods=["GET", "PUT", "POST", "DELETE"])
def notice_controller():
    if request.method == "GET":
        notice = get_notice(request.args.get("notice_id"))
        return jsonify(notice)

    elif request.method == "DELETE":
        delete_notice(request.args.get("notice_id"))
        return jsonify({"status": "ok"})

    elif request.method == "PUT":
        update_notice(request.get_json())
        return jsonify({"status": "ok"})

    elif request.method == "POST":
        id = add_notice(request.get_json())
        return jsonify({"status": "ok", "notice_id": id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
