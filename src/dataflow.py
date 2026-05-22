from src.log import get_logger
from src.schema.io import normalize_io


def check_seq_chain(children: list, job_id: str | None = None) -> list:

    logger = get_logger(job_id)
    warnings = []

    for i in range(len(children) - 1):
        left = children[i]
        right = children[i + 1]

        out_keys = set(normalize_io(left.get("io"))["out"])
        in_keys = set(normalize_io(right.get("io"))["in"])

        if not out_keys or not in_keys:
            continue

        if not (out_keys & in_keys):
            msg = (
                f"dataflow gap: step[{i}] out {sorted(out_keys)} "
                f"-> step[{i+1}] in {sorted(in_keys)}"
            )
            warnings.append(msg)
            logger.warning(msg)

    return warnings
