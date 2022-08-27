from flask import Flask, jsonify
from GetUpcomingContests import get_all
import time

current_li_string = ""
current_dict_list = []
last_update = 0
AUTO_UPDATE_WAIT_TIME = 60 * 60 # 1 hour

app = Flask(__name__)

def fetchLatest():
    global last_update, current_dict_list, current_li_string
    last_update = time.time()
    l = get_all()
    current_li_string = ""
    current_dict_list = []
    for c in l:
        current_li_string += c.toLi()
        current_dict_list.append(c.toDict())

@app.before_request
def before_request():
    global last_update
    if last_update + AUTO_UPDATE_WAIT_TIME <= time.time():
        fetchLatest()

@app.route("/")
def html():
    global last_update, current_li_string
    return f"<h3>Last updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_update))}</h3><ul>{current_li_string}</ul>"

@app.route("/raw")
def raw_data():
    global last_update, current_dict_list
    data = {
        "lastUpdated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_update)),
        "contests": current_dict_list
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
