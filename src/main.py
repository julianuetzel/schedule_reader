import json
import time

from src.schedule_scraper import download_full_schedule
from src.google_calendar import get_creds, update_schedule

if __name__ == "__main__":
    while True:
        with open("config/campusdual.json", mode="r") as json_file:
            userdata = json.load(json_file)
        download_full_schedule(userdata["userid"], userdata["userhash"])
        update_schedule(get_creds())
        time.sleep(86400)  # repeat once a day
