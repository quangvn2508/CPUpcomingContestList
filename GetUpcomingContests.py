import requests
from bs4 import BeautifulSoup
from UpcomingContest import UpcomingContest
import datetime

def get_atcoder():
    l = []
    data = requests.get("https://atcoder.jp")
    atcoder = BeautifulSoup(data.content, 'html.parser')
    for row in atcoder.find(id="contest-table-upcoming").tbody.find_all('tr'):
        contest_time = datetime.datetime.strptime(row.time.contents[0], '%Y-%m-%d %H:%M:%S%z')
        contest_atag = row.find_all('td')[1].a
        contest_name = contest_atag.contents[0]
        contest_url = contest_atag['href']
        l.append(UpcomingContest(contest_time, contest_name, contest_url))
    return l

def get_codeforces():
    l = []
    data = requests.get("https://codeforces.com/api/contest.list")
    json = data.json()
    if json["status"] != "OK":
        return []
    for c in json["result"]:
        if c['relativeTimeSeconds'] >= 0: continue
        l.append(UpcomingContest(datetime.datetime.fromtimestamp(c['startTimeSeconds']), c['name'], f"https://codeforces.com/contests/{c['id']}"))
    return l
