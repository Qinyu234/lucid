# =========================
# FUNCTION: Tree Model
# PURPOSE:
# Store growth graph + semantic + file mapping
# =========================

import time
import uuid


class Node:

    def __init__(
        self,
        name,
        code="",
        path="",
        semantic=""
    ):

        self.id=str(uuid.uuid4())[:8]

        self.name=name

        self.path=path

        self.semantic=semantic

        self.code=code

        self.children=[]

        self.parent=None

        self.status="pending"

        self.created=time.time()

        self.modified=time.time()

    @property
    def completed(self):

        return self.status=="completed"

    @property
    def depth(self):

        d=0

        node=self

        while node.parent:

            d+=1
            node=node.parent

        return d

    def add_child(self,node):

        node.parent=self

        self.children.append(node)

        self.modified=time.time()

    def mark_completed(self):

        self.status="completed"

        self.modified=time.time()

    def update_code(self,code):

        self.code=code

        self.modified=time.time()


def init_tree(seed):

    root=Node(
        name="main",
        code="# generated from idea",
        path="src/main.py",
        semantic=seed["goal"]
    )

    return {
        "root":root,
        "created":time.time(),
        "iteration":0
    }


def is_converged(tree):

    root=tree["root"]

    queue=[root]

    active=0

    max_depth=0

    nodes=0

    while queue:

        node=queue.pop()

        nodes+=1

        max_depth=max(
            max_depth,
            node.depth
        )

        if not node.completed:
            active+=1

        queue.extend(
            node.children
        )

    # 防夜间爆炸

    if nodes>100:
        return True

    if max_depth>6:
        return True

    return active==0