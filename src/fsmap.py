# =========================
# FUNCTION: Filesystem Mapper
# PURPOSE:
# Map tree nodes to real file system
# =========================

import os

ROOT = "output/workplace/src"


def sync_filesystem(tree):

    def dfs(node):

        path = os.path.join(ROOT, node.path)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(node.code)

        for c in node.children:
            dfs(c)

    dfs(tree["root"])