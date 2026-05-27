def topology_catalog(leaf_count: int | None = None, template_id: str | None = None) -> list | dict | None:
    """
    Topology units (minimal): SEQ | PAR | ROUTER — compose into templates per leaf count.

    - topology_catalog(n) -> [{template_id, leaf_count, tree, units}, ...]  for n in 2..6
    - topology_catalog(template_id="seq_4") -> {tree, ...}

    tree shape: {"op": "SEQ"|"PAR"|"ROUTER", "args": [int leaf_index | nested tree]}
    """
    def build_catalog() -> list:
        entries: list = []

        def add(tid: str, n: int, tree: dict, units: str) -> None:
            root = tree.get("op", "SEQ")
            entries.append(
                {
                    "template_id": tid,
                    "leaf_count": n,
                    "tree": tree,
                    "units": units,
                    "topology": root,
                }
            )

        for n in range(2, 7):
            add(f"seq_{n}", n, {"op": "SEQ", "args": list(range(n))}, "SEQ×n")
            add(f"par_{n}", n, {"op": "PAR", "args": list(range(n))}, "PAR×n")
            add(f"router_{n}", n, {"op": "ROUTER", "args": list(range(n))}, "ROUTER×n")

        for n in range(3, 7):
            add(
                f"seq1_par_{n - 1}",
                n,
                {"op": "SEQ", "args": [0, {"op": "PAR", "args": list(range(1, n))}]},
                "SEQ → PAR×(n-1)",
            )
            add(
                f"par_{n - 1}_then_seq1",
                n,
                {
                    "op": "SEQ",
                    "args": [{"op": "PAR", "args": list(range(n - 1))}, n - 1],
                },
                "PAR×(n-1) → SEQ",
            )

        for n in (4, 6):
            half = n // 2
            add(
                f"seq_{half}_seq_{half}",
                n,
                {
                    "op": "SEQ",
                    "args": [
                        {"op": "SEQ", "args": list(range(half))},
                        {"op": "SEQ", "args": list(range(half, n))},
                    ],
                },
                f"SEQ_{half} → SEQ_{half}",
            )

        for n in range(4, 7):
            add(
                f"seq1_par_{n - 2}_seq1",
                n,
                {
                    "op": "SEQ",
                    "args": [
                        0,
                        {"op": "PAR", "args": list(range(1, n - 1))},
                        n - 1,
                    ],
                },
                "SEQ → PAR×(n-2) → SEQ",
            )

        return entries

    catalog = build_catalog()

    if template_id is not None:
        tid = str(template_id).strip()
        for entry in catalog:
            if entry["template_id"] == tid:
                return entry
        return None

    if leaf_count is None:
        return catalog

    n = int(leaf_count)
    return [e for e in catalog if e["leaf_count"] == n]
