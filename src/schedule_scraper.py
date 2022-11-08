import json
import os

import requests as requests

from src import translate_schedule

BASE_URL = "https://selfservice.campus-dual.de"


def download_full_schedule(userid: str, userhash: str):
    url = BASE_URL + "/room/json?userid=" + userid + "&hash=" + userhash

    if requests.get(url, verify=False).status_code != 200:
        print("something went wrong!")
        return None
    with open(os.getenv("DOWNLOAD_PATH", "downloaded.json"), mode="w") as file:
        json.dump(requests.get(url, verify=False).json(), file)

    translate_schedule.sort_out_data("downloaded.json")
