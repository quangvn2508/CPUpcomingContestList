import datetime

class FetchError:
    def __init__(self, msg) -> None:
        self.msg = msg
        self.time = datetime.datetime.now()
    def toLi(self):
        return f"<li>{self.msg}</li>"