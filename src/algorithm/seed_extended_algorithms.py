from pathlib import Path


def seed_extended_algorithms(root: Path):
    def w(path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    w(root / "llm" / "greedy_decode_fixed_vocab.py", _GREEDY)
    w(root / "llm" / "top_k_sample_fixed_vocab.py", _TOPK)
    w(root / "rl" / "epsilon_greedy_fixed_qtable.py", _EPS_GREEDY)
    w(root / "rl" / "q_table_bellman_update.py", _Q_UPDATE)
    w(root / "vision" / "sobel_edge_fixed_kernel.py", _SOBEL)
    w(root / "vision" / "region_mean_fixed_roi.py", _ROI_MEAN)
    w(root / "robotics" / "grid_astar_fixed_map.py", _ASTAR)
    w(root / "robotics" / "differential_drive_step.py", _DRIVE)
    w(root / "calculus" / "trapz_uniform_grid.py", _TRAPZ)
    w(root / "calculus" / "central_diff_uniform.py", _CDIFF)
    w(root / "logic" / "eval_bool_expr_rpn.py", _RPN)
    w(root / "logic" / "truth_table_fixed_inputs.py", _TRUTH)
    w(root / "circuit" / "simulate_logic_netlist.py", _NETLIST)
    w(root / "info_theory" / "entropy_discrete.py", _ENTROPY)
    w(root / "info_theory" / "mutual_information_discrete.py", _MI)
    w(root / "info_theory" / "kl_divergence_discrete.py", _KL)
    w(root / "maxflow" / "edmonds_karp_fixed_graph.py", _MAXFLOW)
    w(root / "collision" / "aabb_overlap_test.py", _AABB)
    w(root / "collision" / "circle_aabb_overlap.py", _CIRCLE_AABB)

_GREEDY = '''# semantic: Greedy argmax over fixed vocabulary logits
# io.in: logits:list
# io.out: token_id:int, token_ids:list

def greedy_decode_fixed_vocab(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    logits = data.get("logits") or []
    if not logits:
        data["token_id"] = 0
        data["token_ids"] = []
        return ctx
    best = max(range(len(logits)), key=lambda i: logits[i])
    data["token_id"] = int(best)
    data["token_ids"] = [int(best)]
    return ctx
'''

_TOPK = '''# semantic: Top-k sample on fixed vocabulary
# io.in: logits:list, k:int, temperature:float, seed:int
# io.out: token_id:int

def top_k_sample_fixed_vocab(ctx):
    import random
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    logits = list(data.get("logits") or [])
    k = max(1, int(data.get("k") or 1))
    temp = float(data.get("temperature") or 1.0) or 1.0
    seed = int(data.get("seed") or 0)
    if not logits:
        data["token_id"] = 0
        return ctx
    pairs = sorted(enumerate(logits), key=lambda x: x[1], reverse=True)[:k]
    idxs, vals = zip(*pairs)
    import math
    m = max(vals)
    exps = [math.exp((v - m) / temp) for v in vals]
    s = sum(exps) or 1.0
    probs = [e / s for e in exps]
    rng = random.Random(seed)
    r = rng.random()
    acc = 0.0
    pick = idxs[0]
    for i, p in zip(idxs, probs):
        acc += p
        if r <= acc:
            pick = i
            break
    data["token_id"] = int(pick)
    return ctx
'''

_EPS_GREEDY = '''# semantic: Epsilon-greedy on fixed Q-table
# io.in: qtable:dict, state:str, epsilon:float, seed:int
# io.out: action:str

def epsilon_greedy_fixed_qtable(ctx):
    import random
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    qtable = data.get("qtable") or {}
    state = str(data.get("state") or "")
    eps = float(data.get("epsilon") or 0.0)
    rng = random.Random(int(data.get("seed") or 0))
    actions = qtable.get(state) or {}
    if not actions:
        data["action"] = ""
        return ctx
    if rng.random() < eps:
        data["action"] = rng.choice(list(actions.keys()))
        return ctx
    data["action"] = max(actions, key=lambda a: actions[a])
    return ctx
'''

_Q_UPDATE = '''# semantic: Tabular Q Bellman backup
# io.in: qtable, state, action, reward, next_state, alpha, gamma, done
# io.out: qtable

def q_table_bellman_update(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    qtable = dict(data.get("qtable") or {})
    s = str(data.get("state") or "")
    a = str(data.get("action") or "")
    r = float(data.get("reward") or 0.0)
    ns = str(data.get("next_state") or "")
    alpha = float(data.get("alpha") or 0.1)
    gamma = float(data.get("gamma") or 0.99)
    done = bool(data.get("done"))
    qtable.setdefault(s, {})
    old = float(qtable[s].get(a, 0.0))
    nxt = 0.0 if done else max((qtable.get(ns) or {}).values() or [0.0])
    qtable[s][a] = old + alpha * (r + gamma * nxt - old)
    data["qtable"] = qtable
    return ctx
'''

_SOBEL = '''# semantic: Sobel edge magnitude on flat grayscale
# io.in: gray:list, width:int, height:int
# io.out: edges:list

def sobel_edge_fixed_kernel(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    gray = data.get("gray") or []
    w = int(data.get("width") or 0)
    h = int(data.get("height") or 0)
    if not gray or w < 3 or h < 3:
        data["edges"] = []
        return ctx
    out = [0.0] * len(gray)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            i = y * w + x
            gx = -gray[i-w-1] + gray[i-w+1] - 2*gray[i-1] + 2*gray[i+1] - gray[i+w-1] + gray[i+w+1]
            gy = -gray[i-w-1] - 2*gray[i-w] - gray[i-w+1] + gray[i+w-1] + 2*gray[i+w] + gray[i+w+1]
            out[i] = float((gx*gx + gy*gy) ** 0.5)
    data["edges"] = out
    return ctx
'''

_ROI_MEAN = '''# semantic: Mean gray in fixed ROI
# io.in: gray, x0, y0, w, h, frame_w
# io.out: mean

def region_mean_fixed_roi(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    gray = data.get("gray") or []
    x0, y0 = int(data.get("x0") or 0), int(data.get("y0") or 0)
    rw, rh = int(data.get("w") or 0), int(data.get("h") or 0)
    fw = int(data.get("frame_w") or 0)
    if not gray or rw <= 0 or rh <= 0 or fw <= 0:
        data["mean"] = 0.0
        return ctx
    total, cnt = 0.0, 0
    for dy in range(rh):
        row = (y0 + dy) * fw + x0
        for dx in range(rw):
            idx = row + dx
            if 0 <= idx < len(gray):
                total += gray[idx]
                cnt += 1
    data["mean"] = float(total / cnt) if cnt else 0.0
    return ctx
'''

_ASTAR = '''# semantic: A* on 4-connected grid (0 free, 1 blocked)
# io.in: grid:list, start:list, goal:list, width:int
# io.out: path:list, cost:float

def grid_astar_fixed_map(ctx):
    import heapq
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    grid = data.get("grid") or []
    start = tuple(data.get("start") or [0, 0])
    goal = tuple(data.get("goal") or [0, 0])
    w = int(data.get("width") or 0)
    if not grid or not w:
        data["path"] = []
        data["cost"] = 0.0
        return ctx

    def h(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def passable(c):
        x, y = c
        if x < 0 or y < 0:
            return False
        i = y * w + x
        return i < len(grid) and grid[i] == 0

    openq = [(h(start, goal), 0, start, [list(start)])]
    seen = set()
    while openq:
        _, g, cur, path = heapq.heappop(openq)
        if cur in seen:
            continue
        seen.add(cur)
        if cur == goal:
            data["path"] = path
            data["cost"] = float(g)
            return ctx
        x, y = cur
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nxt = (x+dx, y+dy)
            if passable(nxt):
                heapq.heappush(openq, (g+1+h(nxt, goal), g+1, nxt, path + [list(nxt)]))
    data["path"] = []
    data["cost"] = 0.0
    return ctx
'''

_DRIVE = '''# semantic: Differential drive pose step
# io.in: x,y,theta,v,omega,dt
# io.out: x,y,theta

def differential_drive_step(ctx):
    import math
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    x = float(data.get("x") or 0.0)
    y = float(data.get("y") or 0.0)
    th = float(data.get("theta") or 0.0)
    v = float(data.get("v") or 0.0)
    om = float(data.get("omega") or 0.0)
    dt = float(data.get("dt") or 0.0)
    th2 = th + om * dt
    x2 = x + v * math.cos(th) * dt
    y2 = y + v * math.sin(th) * dt
    data["x"], data["y"], data["theta"] = x2, y2, th2
    return ctx
'''

_TRAPZ = '''# semantic: Trapezoidal rule on uniform grid
# io.in: y:list, dx:float
# io.out: integral:float

def trapz_uniform_grid(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    y = data.get("y") or []
    dx = float(data.get("dx") or 1.0)
    if len(y) < 2:
        data["integral"] = 0.0
        return ctx
    s = 0.0
    for i in range(len(y)-1):
        s += (y[i] + y[i+1]) * 0.5 * dx
    data["integral"] = float(s)
    return ctx
'''

_CDIFF = '''# semantic: Central difference on uniform grid
# io.in: y:list, dx:float
# io.out: dy:list

def central_diff_uniform(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    y = data.get("y") or []
    dx = float(data.get("dx") or 1.0)
    if len(y) < 3 or dx == 0:
        data["dy"] = []
        return ctx
    out = [0.0] * len(y)
    for i in range(1, len(y)-1):
        out[i] = (y[i+1] - y[i-1]) / (2.0 * dx)
    data["dy"] = out
    return ctx
'''

_RPN = '''# semantic: Evaluate boolean RPN
# io.in: rpn:list, vars:dict
# io.out: value:bool

def eval_bool_expr_rpn(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    rpn = data.get("rpn") or []
    vars_ = data.get("vars") or {}
    stack = []
    for tok in rpn:
        if tok in vars_:
            stack.append(bool(vars_[tok]))
        elif tok == "and":
            b, a = stack.pop(), stack.pop()
            stack.append(a and b)
        elif tok == "or":
            b, a = stack.pop(), stack.pop()
            stack.append(a or b)
        elif tok == "not":
            stack.append(not stack.pop())
        else:
            stack.append(bool(tok))
    data["value"] = bool(stack[-1]) if stack else False
    return ctx
'''

_TRUTH = '''# semantic: Truth table for fixed boolean inputs
# io.in: var_names:list, rpn:list
# io.out: table:list

def truth_table_fixed_inputs(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    names = data.get("var_names") or []
    rpn = data.get("rpn") or []
    n = len(names)
    table = []
    for mask in range(1 << n):
        vars_ = {names[i]: bool((mask >> i) & 1) for i in range(n)}
        stack = []
        for tok in rpn:
            if tok in vars_:
                stack.append(bool(vars_[tok]))
            elif tok == "and":
                b, a = stack.pop(), stack.pop()
                stack.append(a and b)
            elif tok == "or":
                b, a = stack.pop(), stack.pop()
                stack.append(a or b)
            elif tok == "not":
                stack.append(not stack.pop())
            else:
                stack.append(bool(tok))
        table.append({"vars": vars_, "value": bool(stack[-1]) if stack else False})
    data["table"] = table
    return ctx
'''

_NETLIST = '''# semantic: Simulate combinational logic netlist
# io.in: gates:list, inputs:dict  gate: {out, op, in:[names]}
# io.out: outputs:dict

def simulate_logic_netlist(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    gates = data.get("gates") or []
    vals = dict(data.get("inputs") or {})
    for _ in range(len(gates) + 1):
        progressed = False
        for g in gates:
            out = g.get("out")
            if out in vals:
                continue
            ins = g.get("in") or []
            if any(i not in vals for i in ins):
                continue
            op = g.get("op")
            if op == "NOT":
                vals[out] = not bool(vals[ins[0]])
            elif op == "AND":
                vals[out] = all(bool(vals[i]) for i in ins)
            elif op == "OR":
                vals[out] = any(bool(vals[i]) for i in ins)
            elif op == "XOR":
                v = False
                for i in ins:
                    v = v ^ bool(vals[i])
                vals[out] = v
            progressed = True
        if not progressed:
            break
    data["outputs"] = vals
    return ctx
'''

_ENTROPY = '''# semantic: Shannon entropy H(X)
# io.in: probs:dict
# io.out: entropy:float

def entropy_discrete(ctx):
    import math
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    probs = data.get("probs") or {}
    h = 0.0
    for p in probs.values():
        p = float(p)
        if p > 0:
            h -= p * math.log2(p)
    data["entropy"] = float(h)
    return ctx
'''

_MI = '''# semantic: Mutual information I(X;Y) from joint counts
# io.in: joint:dict  key "x|y" -> count
# io.out: mi:float

def mutual_information_discrete(ctx):
    import math
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    joint = data.get("joint") or {}
    total = sum(joint.values()) or 1.0
    px, py = {}, {}
    for k, c in joint.items():
        x, y = k.split("|", 1)
        px[x] = px.get(x, 0) + c
        py[y] = py.get(y, 0) + c
    mi = 0.0
    for k, c in joint.items():
        x, y = k.split("|", 1)
        pxy = c / total
        if pxy > 0:
            mi += pxy * math.log2(pxy * total / (px[x] * py[y]))
    data["mi"] = float(mi)
    return ctx
'''

_KL = '''# semantic: KL divergence D(P||Q)
# io.in: p:dict, q:dict
# io.out: kl:float

def kl_divergence_discrete(ctx):
    import math
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    p = data.get("p") or {}
    q = data.get("q") or {}
    kl = 0.0
    for k, pv in p.items():
        pv = float(pv)
        qv = float(q.get(k, 0.0))
        if pv > 0 and qv > 0:
            kl += pv * math.log2(pv / qv)
    data["kl"] = float(kl)
    return ctx
'''

_MAXFLOW = '''# semantic: Edmonds-Karp max flow
# io.in: adj:dict  u -> {v: cap}, source, sink
# io.out: max_flow, flow dict u|v

def edmonds_karp_fixed_graph(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    adj = data.get("adj") or {}
    s = str(data.get("source") or "")
    t = str(data.get("sink") or "")
    flow = {}
    maxf = 0.0

    def cap(u, v):
        return float((adj.get(u) or {}).get(v, 0.0))

    def residual(u, v):
        return cap(u, v) - flow.get(f"{u}|{v}", 0.0) + flow.get(f"{v}|{u}", 0.0)

    while True:
        parent = {s: None}
        q = [s]
        for u in q:
            for v in (adj.get(u) or {}):
                if v not in parent and residual(u, v) > 1e-12:
                    parent[v] = u
                    q.append(v)
            for v in adj:
                if v not in parent and residual(v, u) > 1e-12:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            break
        path_flow = float("inf")
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, residual(u, v))
            v = u
        v = t
        while v != s:
            u = parent[v]
            key = f"{u}|{v}"
            flow[key] = flow.get(key, 0.0) + path_flow
            rev = f"{v}|{u}"
            if rev in flow:
                flow[rev] -= path_flow
            v = u
        maxf += path_flow
    data["max_flow"] = float(maxf)
    data["flow"] = flow
    return ctx
'''

_AABB = '''# semantic: 2D AABB overlap  box: {x,y,w,h}
# io.in: a:dict, b:dict
# io.out: hit:bool

def aabb_overlap_test(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    a, b = data.get("a") or {}, data.get("b") or {}
    ax, ay, aw, ah = float(a.get("x",0)), float(a.get("y",0)), float(a.get("w",0)), float(a.get("h",0))
    bx, by, bw, bh = float(b.get("x",0)), float(b.get("y",0)), float(b.get("w",0)), float(b.get("h",0))
    hit = ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by
    data["hit"] = bool(hit)
    return ctx
'''

_CIRCLE_AABB = '''# semantic: Circle vs AABB overlap
# io.in: circle:{x,y,r}, box:{x,y,w,h}
# io.out: hit:bool

def circle_aabb_overlap(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    c, b = data.get("circle") or {}, data.get("box") or {}
    cx, cy, r = float(c.get("x",0)), float(c.get("y",0)), float(c.get("r",0))
    bx, by, bw, bh = float(b.get("x",0)), float(b.get("y",0)), float(b.get("w",0)), float(b.get("h",0))
    nx = max(bx, min(cx, bx + bw))
    ny = max(by, min(cy, by + bh))
    dx, dy = cx - nx, cy - ny
    data["hit"] = bool(dx*dx + dy*dy <= r*r)
    return ctx
'''
