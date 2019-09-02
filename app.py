from flask import Flask, request, jsonify
from db import *

app = Flask(__name__)

# Does nothing
@app.route('/')
def index():
    return jsonify({
        "status":"ok"
    })

@app.route("/events")
def events_controller():
    return jsonify(get_events())

@app.route("/event", methods=["GET"])
def event_controller():
    if request.method=="GET":
        events = get_event(request.args.get("event_id"))
        return jsonify(events)

    elif request.method=="DELETE":
        delete_event(request.args.get("event_id"))
        return jsonify({"status":"ok"})

    elif request.method=="PUT":
        update_event(request.get_json())
        return jsonify({"status":"ok"})

    elif request.method=="POST":
        add_event(request.get_json())
        return jsonify({"status":"ok"})


@app.route("/regs")
def regs_controller():
    if "email" in request.args:
        return jsonify({"status":"error","error":"method not implemented yet."})

    elif "event_id" in request.args:
        if "status" in request.args:
            regs = get_regs(request.args.get("event_id"),request.args.get("status"))
        else:
            regs = get_regs(request.args.get("event_id"))
        return jsonify(regs)


@app.route("/reg", methods=["GET","PUT","POST","DELETE"])
def reg_controller():
    if request.method=="GET":
        reg = get_reg(request.args.get("reg_id"))
        return jsonify(reg)

    elif request.method=="DELETE":
        delete_reg(request.args.get("reg_id"))
        return jsonify({"status":"ok"})

    elif request.method=="POST":
        add_reg(request.get_json())
        return jsonify({"status":"ok"})


if __name__ == '__main__':
    # session["login"] = False

    app.run(host='0.0.0.0', debug=True)
