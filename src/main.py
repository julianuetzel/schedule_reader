import json

from src.schedule_scraper import Scraper

if __name__ == "__main__":
    with open("config/campusdual.json", mode="r") as json_file:
        username = json.load(json_file)["username"]
        userhash = json.load(json_file)["hash"]

    Scraper(username=username, userhash=userhash).download_full_schedule()


