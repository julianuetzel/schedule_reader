import json
import os

unknown_dozent = list()
PREPEND_TITLES = False


def sort_out_data(input_file: str, output_file: str):
    with open(input_file, mode="r") as i_file:
        sched_data = json.load(i_file)

    del_fields = []
    # unnecessary fields
    del_fields += ["sroom", "sinstructor", "description", "allDay", "color", "editable"]

    for lesson in sched_data:
        for field in del_fields:
            del lesson[field]

    for lesson in sched_data:

        date = lesson["start"].split(" ")[0]
        if date != lesson["start"].split(" ")[0]:
            print("parsing error! start and end date do not match! ", lesson)
            continue
        lesson["date"] = date

        for time in ("start", "end"):
            lesson[time] = lesson[time].split(" ")[1]

    for lesson in sched_data:
        if not room_valid(lesson["room"]):
            lesson["room"], lesson["remarks"] = room_and_remarks_from_remarks(lesson["remarks"])

    for lesson in sched_data:
        lesson["instructor"] = dozent_translate(lesson["instructor"])

    for dozent in unknown_dozent:
        print("unknown instructor ", dozent)

    with open(output_file, mode="w") as o_file:
        json.dump(sched_data, o_file)


def room_valid(room: str):
    # Special rooms
    if room in ("AULA", "Z_TI1", "Z_TI2", "Z_TI3", "____"):
        return True

    # Last 3 characters have to be int
    try:
        _ = int(room[-3:])
    except ValueError:
        return False

    # Before hast to be identifier
    if room[:-3] not in ("VR", "SR", "PC", "L"):
        return False

    return True


def room_and_remarks_from_remarks(remarks: str):
    homeschooling_tags = ["Fernlehre", "Fernstudium", "Selbststudium"]
    room = "unknown room. an error might have occured."
    sp = remarks.replace("(", "").replace(")", " ").split(" ")
    # if 2 words or unknown room
    if len(sp) > 2 or not room_valid(sp[0]):
        # if remarks in homeschooling_tags
        if any([x in remarks for x in homeschooling_tags]):
            for x in homeschooling_tags:
                remarks = remarks.replace(x, "")
            return "zuhause :)", remarks
        print("unable to parse room for remarks: ", remarks)
        return room, remarks
    room = sp[0]
    remarks = " ".join(sp[1:])
    return room, remarks


def dozent_translate(name: str):
    with open(os.getenv("DOZENT_CONFIG", "config/dozent.json"), mode="r") as file:
        dozents = json.load(file)

    for dozent in dozents:
        for alias in dozent["alias"]:
            if alias == name:
                if PREPEND_TITLES:
                    return dozent["title"] + " " + dozent["name"]
                return dozent["name"]
    if name not in unknown_dozent:
        unknown_dozent.append(name)
        return "unknown (" + name + ")"
