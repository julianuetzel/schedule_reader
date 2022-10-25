import json

unknown_dozent = list()


def sort_out_data(input_file: str, output_file: str):
    with open(input_file, mode="r") as i_file:
        sched_data = json.load(i_file)

    del_fields = []
    # unnecessary fields
    del_fields += ["sroom", "sinstructor", "description", "allDay", "color", "editable"]

    print("deleting fields: ", del_fields)
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
    return True


def room_and_remarks_from_remarks(remarks: str):
    return "room", "remarks"


def dozent_translate(name: str):
    return "dozent"
