from flask import Flask
from GetUpcomingContests import get_atcoder, get_codeforces, get_leetcode, get_vnoj
import webbrowser

app = Flask(__name__)

@app.route("/")
def hello_world():
    li = ""
    l = []
    l.extend(get_atcoder())
    l.extend(get_codeforces())
    l.extend(get_leetcode())
    l.extend(get_vnoj())
    for c in sorted(l, key=lambda _c : _c.time.timestamp()):
        li += c.toLi()
    return "<ul>" + li + "</ul>"

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    open_browser()
    app.run(debug=True, use_reloader=False)