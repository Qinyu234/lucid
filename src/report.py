# =========================
# MODULE: report
# FUNCTION: report
#
# PURPOSE:
# report execution result per job
# =========================


def report(job, result):

    print("\n====================")

    print("JOB:", job["id"])

    print("STATUS:", result.get("status", "unknown"))

    print("ITER:", result.get("iteration", 0))

    if "message" in result:

        print("MESSAGE:", result["message"])