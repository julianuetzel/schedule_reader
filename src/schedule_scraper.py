import json
import os
from pathlib import Path

import requests as requests

from src import translate_schedule

BASE_URL = "https://selfservice.campus-dual.de"


class Scraper:
    TEMP_DIR = "./temp"
    DATA_DIR = "./data"

    def __init__(self, username: str, userhash: str):
        self.USERHASH = userhash
        self.USERNAME = username
        self.TEMP_DIR = self.TEMP_DIR.replace(".", os.path.dirname(os.path.dirname(__file__))) + "/" + username + "/"
        self.DATA_DIR = self.DATA_DIR.replace(".", os.path.dirname(os.path.dirname(__file__))) + "/" + username + "/"
        print(self.TEMP_DIR, self.DATA_DIR)
        Path(self.TEMP_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.DATA_DIR).mkdir(parents=True, exist_ok=True)

    def download_full_schedule(self):
        url = BASE_URL + "/room/json?userid=" + self.USERNAME + "&hash=" + self.USERHASH
        if requests.get(url).status_code != 200:
            print("error querying json api!")
            return
        with open(file=(self.DATA_DIR + "downloaded.json"), mode= "w") as file:
            json.dump(requests.get(url).json(), file)
        translate_schedule.sort_out_data(self.DATA_DIR + "downloaded.json", self.DATA_DIR + "schedule.json")
