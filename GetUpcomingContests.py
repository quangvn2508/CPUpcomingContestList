import requests
from bs4 import BeautifulSoup
from UpcomingContest import UpcomingContest
from Error import FetchError
import datetime
import json

def get_atcoder():
    l = []
    data = requests.get("https://atcoder.jp")
    atcoder = BeautifulSoup(data.content, 'html.parser')
    for row in atcoder.find(id="contest-table-upcoming").tbody.find_all('tr'):
        contest_time = datetime.datetime.strptime(row.time.contents[0], '%Y-%m-%d %H:%M:%S%z')
        contest_atag = row.find_all('td')[1].a
        contest_name = contest_atag.contents[0]
        contest_url = f"https://atcoder.jp{contest_atag['href']}"
        l.append(UpcomingContest(contest_time, contest_name, contest_url))
    return l

def get_codeforces():
    l = []
    data = requests.get("https://codeforces.com/api/contest.list")
    try:
        _json = data.json()
        if _json["status"] != "OK":
            return []
        for c in _json["result"]:
            if c['relativeTimeSeconds'] >= 0: continue
            l.append(UpcomingContest(datetime.datetime.fromtimestamp(c['startTimeSeconds']), c['name'], f"https://codeforces.com/contests/{c['id']}"))
    except json.decoder.JSONDecodeError:
        l.append(FetchError(data.text))
    return l

def get_leetcode():
    data = requests.get("https://leetcode.com/contest/")
    lc = BeautifulSoup(data.content, 'html.parser')
    _json = json.loads(lc.find(id="__NEXT_DATA__").contents[0])
    contest_list = None
    for q in _json["props"]["pageProps"]["dehydratedState"]["queries"]:
        if "topTwoContests" in q["queryKey"]:
            contest_list = q["state"]["data"]["topTwoContests"]
    l = []
    for c in contest_list:
        l.append(UpcomingContest(datetime.datetime.fromtimestamp(c['startTime']), c['title'], f"https://leetcode.com/contest/{c['titleSlug']}"))
    return l

def get_vnoj():
    data = requests.get("https://oj.vnoi.info/contests/", headers={'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'})
    vnoj = BeautifulSoup(data.content, 'html.parser')
    l = []

    upcoming_contest_component = vnoj.find("h4", string="Upcoming Contests")
    if upcoming_contest_component == None: return l

    table_body = upcoming_contest_component.find_next_sibling().find("tbody")
    if table_body == None: return l

    for row in table_body.find_all('tr'):
        if row.find("span", class_="contest-tag") == None: # If rated, span with class contest-tag exist
            continue
        contest_atag = row.find('a')
        contest_time_string = row.find('div', class_="time-left").contents[0] # MMM D, YYYY, HH:mm
        start_time_string = contest_time_string[1:contest_time_string.find("<br/>")]
        l.append(UpcomingContest(datetime.datetime.strptime(start_time_string + " +0700", '%b %d, %Y, %H:%M %z'), contest_atag.contents[0], f"https://oj.vnoi.info{contest_atag['href']}"))
    return l
import traceback
def get_all():
    l = []
    try:
        l.extend(get_atcoder())
        l.extend(get_codeforces())
        l.extend(get_leetcode())
        l.extend(get_vnoj())
    except:
        f = open('log.txt', 'a')
        f.write("Error at " + datetime.datetime.now().strftime('%d-%m-%Y %H:%M %z') + "\n")
        f.write(traceback.format_exc())
        f.write("---")
    return sorted(l, key=lambda _c : _c.time.timestamp())
