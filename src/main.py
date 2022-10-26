import json

from src.schedule_scraper import download_full_schedule

if __name__ == "__main__":
    with open("config/campusdual.json", mode="r") as json_file:
        userdata = json.load(json_file)
    userid, userhash = userdata["userid"], userdata["userhash"]
    print("userid: ", userid, "userhash: ", userhash)
    download_full_schedule(userid, userhash)

