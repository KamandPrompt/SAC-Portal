from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/",)
def create_event():
    data=request.get_json()
    event_name=data["event_name"]
    date=data["date"]
    time=data["time"]
    about=data["about"]
    return jsonify({"result":"event_created", "event_name":event_name, "date":date, "time":time, "about":about})


if __name__ == "__main__":
    app.run(debug=True)

