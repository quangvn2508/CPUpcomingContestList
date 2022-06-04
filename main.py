from flask import Flask
from GetUpcomingContests import get_atcoder, get_codeforces

app = Flask(__name__)

@app.route("/")
def hello_world():
    li = ""
    l = []
    l.extend(get_atcoder())
    l.extend(get_codeforces())
    for c in sorted(l, key=lambda _c : _c.time.timestamp()):
        li += c.toLi()
    return "<ul>" + li + "</ul>"

if __name__ == '__main__':
    app.run(debug=True)