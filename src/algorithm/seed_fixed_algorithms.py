from pathlib import Path


def seed_fixed_algorithms(root: Path):
    def write_module(path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    write_module(
        root / "encoding" / "huffman_known_weights.py",
        '''# semantic: Huffman codebook for FIXED known symbol weights per session
# fixed.profile: telemetry_skewed_symbols
# fixed.distribution: categorical i.i.d.; weights static within session
# fixed.business: compress repeated telemetry / game event codes
# advantage.vs: fixed_width_code
# advantage.margin: bits/symbol -> H(X) vs ceil(log2(K))
# io.in: symbols:list, weights:dict
# io.out: codebook:dict, expected_bits:float

def huffman_known_weights(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    symbols = data.get("symbols") or []
    weights = data.get("weights") or {}
    if not symbols or not weights:
        data["codebook"] = {}
        data["expected_bits"] = 0.0
        return ctx
    import heapq
    nodes = [[w, [s, ""]] for s, w in weights.items() if s in symbols]
    heapq.heapify(nodes)
    while len(nodes) > 1:
        a = heapq.heappop(nodes)
        b = heapq.heappop(nodes)
        for pair in a[1:]:
            pair[1] = "0" + pair[1]
        for pair in b[1:]:
            pair[1] = "1" + pair[1]
        heapq.heappush(nodes, [a[0] + b[0]] + a[1:] + b[1:])
    codebook = {sym: code for sym, code in nodes[0][1:]}
    total = sum(weights.values()) or 1.0
    expected = sum(weights[s] * len(codebook.get(s, "")) for s in codebook) / total
    data["codebook"] = codebook
    data["expected_bits"] = float(expected)
    return ctx
''',
    )

    write_module(
        root / "encoding" / "run_length_sparse_alphabet.py",
        '''# semantic: Run-length encoding when alphabet size K is FIXED and runs are common
# fixed.profile: sparse_run_events
# fixed.distribution: symbols from fixed alphabet; P(run) high, i.i.d. across frames
# fixed.business: delta logging of repeated game states / blank frames
# advantage.vs: raw_symbol_stream
# advantage.margin: O(run) storage vs O(n) when run-length >> 1
# io.in: symbols:list
# io.out: rle_pairs:list

def run_length_sparse_alphabet(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    symbols = data.get("symbols") or []
    if not symbols:
        data["rle_pairs"] = []
        return ctx
    pairs = []
    cur = symbols[0]
    count = 1
    for s in symbols[1:]:
        if s == cur:
            count += 1
        else:
            pairs.append([cur, count])
            cur = s
            count = 1
    pairs.append([cur, count])
    data["rle_pairs"] = pairs
    return ctx
''',
    )

    write_module(
        root / "vision" / "grid_cell_reader.py",
        '''# semantic: Read FIXED grid cell at (row,col) from uniform screen buffer
# fixed.profile: ocr_fixed_hud_grid
# fixed.distribution: pixel patches i.i.d. noise; cell layout static across sessions
# fixed.business: OCR game HUD / logger UI with fixed template positions
# advantage.vs: full_screen_ocr
# advantage.margin: O(1) cell crop vs O(W*H) when layout is known
# io.in: frame:bytes, row:int, col:int, cell_w:int, cell_h:int
# io.out: cell_patch:bytes

def grid_cell_reader(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    frame = data.get("frame") or b""
    row = int(data.get("row") or 0)
    col = int(data.get("col") or 0)
    cell_w = int(data.get("cell_w") or 1)
    cell_h = int(data.get("cell_h") or 1)
    if not frame:
        data["cell_patch"] = b""
        return ctx
    width = int(data.get("width") or max(cell_w, 1))
    start = (row * cell_h) * width + (col * cell_w)
    end = start + cell_w * cell_h
    data["cell_patch"] = frame[start:end] if start < len(frame) else b""
    return ctx
''',
    )

    write_module(
        root / "analytics" / "histogram_delta_encode.py",
        '''# semantic: Delta-encode FIXED-bin histogram when totals drift slowly
# fixed.profile: game_stat_histogram
# fixed.distribution: bin counts change slowly frame-to-frame; bin edges FIXED
# fixed.business: game analytics / stat aggregation with stable schema
# advantage.vs: raw_histogram_json
# advantage.margin: sparse deltas vs full vector when drift is small
# io.in: prev_counts:list, counts:list
# io.out: deltas:list

def histogram_delta_encode(ctx):
    data = ctx.setdefault("data", {})
    ctx.setdefault("meta", {})
    ctx.setdefault("state", {})
    ctx.setdefault("error", None)
    prev = data.get("prev_counts") or []
    cur = data.get("counts") or []
    n = max(len(prev), len(cur))
    deltas = []
    for i in range(n):
        a = prev[i] if i < len(prev) else 0
        b = cur[i] if i < len(cur) else 0
        deltas.append(b - a)
    data["deltas"] = deltas
    return ctx
''',
    )
