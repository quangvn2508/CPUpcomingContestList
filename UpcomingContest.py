import datetime

class UpcomingContest:
    def __init__(self, time: datetime, name, url) -> None:
        self.time = time.astimezone()
        self.name = name
        self.url = url
    def toLi(self):
        return ("<li>"
            f"<span>[{self.time.strftime('%d-%m-%Y %H:%M %z')}]:</span>&nbsp;"
            f"<a href='{self.url}'>{self.name}</a>"
            "</li>")