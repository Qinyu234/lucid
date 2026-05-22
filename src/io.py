# =========================
# MODULE: io
# FUNCTION: io
#
# PURPOSE:
# read json input for runtime system
# =========================


import json


def io():

    path = "input/idea_list.json"

    file = open(path, "r", encoding="utf-8")

    data = json.load(file)

    file.close()

    return data