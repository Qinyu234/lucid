# =========================
# MODULE: validator
# FUNCTION: validator
#
# PURPOSE:
# validate input json structure
# =========================


def validator(data):

    if not isinstance(data, dict):
        return False

    if "jobs" not in data:
        return False

    for job in data["jobs"]:

        if "id" not in job or job["id"] == "":
            return False

        if "goal" not in job or job["goal"] == "":
            return False

        if "language" not in job or job["language"] == "":
            job["language"] = "python"

        if "root_path" not in job or job["root_path"] == "":
            return False

    return True