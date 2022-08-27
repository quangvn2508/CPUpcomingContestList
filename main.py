from flask import Flask
from GetUpcomingContests import get_all_as_li
import time

current_contests_list = ""
last_update = 0
AUTO_UPDATE_WAIT_TIME = 60 * 60 # 1 hour

app = Flask(__name__)

@app.route("/")
def hello_world():
    global current_contests_list, last_update
    if last_update + AUTO_UPDATE_WAIT_TIME <= time.time():
        last_update = time.time()
        current_contests_list = get_all_as_li()
    return f"<h3>Last updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_update))}</h3><ul>{current_contests_list}</ul>"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

