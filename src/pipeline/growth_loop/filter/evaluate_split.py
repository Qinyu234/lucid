def evaluate_split(parent_semantic: str, proposal: list) -> tuple:
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.lib.cosine_similarity_util import cosine_similarity_util
    from src.shared.lib.feature_util import feature_util
    from src.shared.lib.re_util import re_util
    from src.shared.lib.sentence_transformer_encode_util import sentence_transformer_encode_util
    from src.shared.validate.io_in_names_util import io_in_names_util
    from src.shared.validate.io_out_names_util import io_out_names_util

    """
    Validate LLM split; score SEQ / PAR / ROUTER fit from semantics, IO keys, lexical overlap.

    Returns (valid, reason, accepted, analysis).
  analysis.embed_log is a multi-line block for system logs (定位).
    """

    def _growth_cfg() -> dict:
        return app_config_util().get("growth", {})

    def _analysis_cfg() -> dict:
        return _growth_cfg().get("split_analysis") or {}

    def _max_children() -> int:
        return int(_growth_cfg().get("max_children", 6))

    def _validation_mode() -> str:
        cfg = _growth_cfg()
        mode = str(cfg.get("split_validation", "") or "").strip().lower()
        if mode in ("off", "light", "embedding", "analysis"):
            return mode
        if feature_util("embedding_split"):
            return "embedding"
        return "analysis"

    def _token_set(text: str) -> set:
        re = re_util()
        return set(re.findall(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]+", str(text).lower()))

    def _jaccard(a: str, b: str) -> float:
        ta, tb = (_token_set(a), _token_set(b))
        if not ta and not tb:
            return 1.0
        if not ta or not tb:
            return 0.0
        inter = len(ta & tb)
        union = len(ta | tb)
        return inter / union if union else 0.0

    def _threshold() -> float:
        return float(_growth_cfg().get("similarity_threshold", 0.85))

    def _proposal_items(proposal: list) -> list:
        return [p for p in proposal if isinstance(p, dict) and p.get("semantic")]

    def _step_io_sets(item: dict) -> tuple:
        io = item.get("io") or {}
        return (set(io_in_names_util(io)), set(io_out_names_util(io)))

    def _split_analysis(parent_semantic: str, items: list) -> dict:
        acfg = _analysis_cfg()
        parent = str(parent_semantic or "").strip()
        n = len(items)
        parent_max = float(_growth_cfg().get("parent_overlap_max", 0.92))
        sibling_max = float(_growth_cfg().get("sibling_overlap_max", 0.95))
        min_plausibility = float(acfg.get("min_plausibility", 0.25))

        parent_overlaps = []
        for i, p in enumerate(items):
            sem = str(p.get("semantic", ""))
            ov = _jaccard(parent, sem) if parent else 0.0
            parent_overlaps.append(round(ov, 4))

        sibling_pairs = []
        max_sibling_j = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                sj = _jaccard(
                    str(items[i].get("semantic", "")),
                    str(items[j].get("semantic", "")),
                )
                max_sibling_j = max(max_sibling_j, sj)
                sibling_pairs.append({"i": i, "j": j, "jaccard": round(sj, 4)})

        ins, outs = [], []
        for p in items:
            i_set, o_set = _step_io_sets(p)
            ins.append(i_set)
            outs.append(o_set)

        chain_ratios = []
        for i in range(max(0, n - 1)):
            nxt_in = ins[i + 1]
            if not nxt_in:
                chain_ratios.append(0.5)
            else:
                chain_ratios.append(len(outs[i] & nxt_in) / len(nxt_in))
        seq_chain = sum(chain_ratios) / len(chain_ratios) if chain_ratios else 0.0

        cross_io_deps = 0
        for i in range(n):
            for j in range(i + 1, n):
                if outs[i] & ins[j]:
                    cross_io_deps += 1
        pairs = max(1, n * (n - 1) // 2)
        par_no_seq_dep = 1.0 - min(1.0, cross_io_deps / pairs)

        union_in = set()
        for s in ins:
            union_in |= s
        shared_in = ins[0]
        for s in ins[1:]:
            shared_in = shared_in & s
        par_shared_in = (len(shared_in) / len(union_in)) if union_in else 0.0

        tags = []
        for p in items:
            t = p.get("tag") or p.get("case")
            tags.append(str(t).strip() if t else "")
        distinct_tags = len({t for t in tags if t})
        router_tag_ratio = distinct_tags / n if n else 0.0

        mean_parent_ov = sum(parent_overlaps) / n if n else 0.0
        if mean_parent_ov >= parent_max:
            plausibility = 0.0
        elif mean_parent_ov < 0.08:
            plausibility = 0.35
        else:
            plausibility = max(0.0, 1.0 - abs(mean_parent_ov - 0.42) / 0.58)

        lexical_ok = max_sibling_j < sibling_max
        copy_parent = all((ov >= parent_max for ov in parent_overlaps)) if parent_overlaps else False

        out_sigs = [frozenset(o) for o in outs]
        io_out_collision = False
        collision_keys = []
        if n >= 2:
            seen_out: dict = {}
            for i, sig in enumerate(out_sigs):
                if not sig:
                    continue
                if sig in seen_out:
                    io_out_collision = True
                    collision_keys.append(sorted(sig))
                else:
                    seen_out[sig] = i
            for i in range(n):
                for j in range(i + 1, n):
                    if outs[i] & outs[j] and outs[i] == outs[j] and outs[i]:
                        io_out_collision = True

        topology_scores = {
            "SEQ": round(
                seq_chain * plausibility * (0.4 + 0.6 * (1.0 - max_sibling_j)) * (1.0 if n >= 2 else 0.5),
                4,
            ),
            "PAR": round(
                (0.5 * par_no_seq_dep + 0.5 * par_shared_in)
                * plausibility
                * (1.0 - 0.35 * seq_chain)
                * (1.0 if n >= 2 else 0.0),
                4,
            ),
            "ROUTER": round(
                router_tag_ratio * plausibility * (1.2 if distinct_tags >= 2 else 0.25),
                4,
            ),
        }
        if seq_chain >= 0.55:
            topology_scores["SEQ"] = round(topology_scores["SEQ"] * 1.35, 4)
            topology_scores["PAR"] = round(topology_scores["PAR"] * 0.35, 4)
        if io_out_collision:
            topology_scores["PAR"] = round(topology_scores["PAR"] * 0.2, 4)

        recommended_topology = max(topology_scores, key=topology_scores.get)

        tid = f"{recommended_topology.lower()}_{n}"
        if recommended_topology == "SEQ" and n >= 3 and seq_chain < 0.35 and par_no_seq_dep > 0.6:
            tid = f"seq1_par_{n - 1}"
        if recommended_topology == "SEQ" and n in (4, 6) and seq_chain >= 0.5:
            half = n // 2
            tid = f"seq_{half}_seq_{half}"

        reject_collision = bool(acfg.get("reject_io_out_collision", True))
        keep_split = (
            n >= int(_growth_cfg().get("min_children", 2))
            and not copy_parent
            and lexical_ok
            and plausibility >= min_plausibility
            and max(topology_scores.values()) >= float(acfg.get("min_topology_score", 0.15))
            and (not io_out_collision or not reject_collision)
        )

        step_lines = []
        for i, p in enumerate(items):
            i_set, o_set = _step_io_sets(p)
            step_lines.append(
                f"  [{i}] semantic={str(p.get('semantic', ''))[:80]!r} "
                f"in={sorted(i_set)!r} out={sorted(o_set)!r} "
                f"parent_j={parent_overlaps[i] if i < len(parent_overlaps) else 0} tag={tags[i]!r}"
            )

        embed_log = "\n".join(
            [
                "=== split analysis (system) ===",
                f"parent_semantic: {parent[:200]!r}",
                f"steps({n}):",
                *step_lines,
                f"lexical: max_sibling_jaccard={round(max_sibling_j, 4)} ok={lexical_ok} "
                f"parent_overlap={parent_overlaps} copy_parent={copy_parent}",
                f"io: seq_chain={round(seq_chain, 4)} par_no_seq_dep={round(par_no_seq_dep, 4)} "
                f"par_shared_in={round(par_shared_in, 4)} router_tags={distinct_tags}/{n} "
                f"io_out_collision={io_out_collision} keys={collision_keys[:3]}",
                f"plausibility={round(plausibility, 4)} keep_split={keep_split}",
                f"topology_scores={topology_scores} -> {recommended_topology} template={tid}",
                "=== end split analysis ===",
            ]
        )

        return {
            "keep_split": keep_split,
            "plausibility": round(plausibility, 4),
            "lexical_ok": lexical_ok,
            "copy_parent": copy_parent,
            "max_sibling_jaccard": round(max_sibling_j, 4),
            "parent_overlaps": parent_overlaps,
            "sibling_pairs": sibling_pairs[:12],
            "seq_chain_score": round(seq_chain, 4),
            "par_no_seq_dep": round(par_no_seq_dep, 4),
            "par_shared_in": round(par_shared_in, 4),
            "router_tag_ratio": round(router_tag_ratio, 4),
            "topology_scores": topology_scores,
            "recommended_topology": recommended_topology,
            "recommended_template_id": tid,
            "io_out_collision": io_out_collision,
            "embed_log": embed_log,
        }

    def _dedupe_siblings_embed(items: list, threshold: float | None = None) -> list:
        threshold = threshold or _threshold()
        vectors = []
        result = []
        for p in items:
            vec = sentence_transformer_encode_util(p.get("semantic", ""))
            if not vec:
                result.append(p)
                continue
            if any(cosine_similarity_util(vec, v) > threshold for v in vectors):
                continue
            vectors.append(vec)
            result.append(p)
        return result

    def _accept_light(parent_semantic: str, items: list, analysis: dict) -> tuple:
        max_children = _max_children()
        cfg = _growth_cfg()
        parent_max = float(cfg.get("parent_overlap_max", 0.92))
        sibling_max = float(cfg.get("sibling_overlap_max", 0.95))
        parent = str(parent_semantic or "").strip()
        pool = list(items)
        if parent:
            filtered = [p for p in pool if _jaccard(str(p.get("semantic", "")), parent) < parent_max]
            if filtered:
                pool = filtered
        accepted = []
        for p in pool:
            sem = str(p.get("semantic", ""))
            if any(_jaccard(sem, str(a.get("semantic", ""))) >= sibling_max for a in accepted):
                continue
            accepted.append(p)
        if not accepted:
            accepted = pool[:max_children]
        if not accepted:
            accepted = items[:max_children]
        if not analysis.get("keep_split", True):
            reason = "io_out_collision" if analysis.get("io_out_collision") else "analysis_reject"
            return (False, reason, [], analysis)
        return (True, "ok", accepted[:max_children], analysis)

    def _accept_off(items: list, analysis: dict) -> tuple:
        max_children = _max_children()
        seen = set()
        accepted = []
        for p in items:
            key = str(p.get("semantic", "")).strip().lower()
            if key in seen:
                continue
            seen.add(key)
            accepted.append(p)
        if not accepted:
            accepted = items[:max_children]
        return (True, "ok", accepted[:max_children], analysis)

    def _accept_embedding(parent_semantic: str, items: list, analysis: dict) -> tuple:
        max_children = _max_children()
        if not parent_semantic:
            deduped = _dedupe_siblings_embed(items)
            acc = deduped if deduped else items[:max_children]
            return (True, "embed_unavailable", acc, analysis)
        threshold = _threshold()
        parent_vec = sentence_transformer_encode_util(str(parent_semantic))
        if not parent_vec:
            return (True, "embed_unavailable", items[:max_children], analysis)
        scored = []
        for p in items:
            vec = sentence_transformer_encode_util(p.get("semantic", ""))
            if not vec:
                scored.append((p, 0.0))
                continue
            scored.append((p, cosine_similarity_util(vec, parent_vec)))
        if scored and all(sim > threshold for _, sim in scored):
            return (False, "all_steps_similar_to_parent", [], analysis)
        distinct = [p for p, sim in scored if sim <= threshold]
        if not distinct:
            return (False, "no_distinct_steps", [], analysis)
        accepted = _dedupe_siblings_embed(distinct, threshold)
        if not accepted:
            return (False, "siblings_collapsed", [], analysis)
        cfg = _growth_cfg()
        if not cfg.get("dedupe_siblings", True):
            accepted = distinct
        if not analysis.get("keep_split", True):
            reason = "io_out_collision" if analysis.get("io_out_collision") else "analysis_reject"
            return (False, reason, [], analysis)
        return (True, "ok", accepted[:max_children], analysis)

    def _accept_analysis(parent_semantic: str, items: list, analysis: dict) -> tuple:
        return _accept_light(parent_semantic, items, analysis)

    items = _proposal_items(proposal)
    analysis = _split_analysis(parent_semantic, items)
    if not items:
        analysis["keep_split"] = False
        return (False, "empty_proposal", [], analysis)

    mode = _validation_mode()
    if mode == "off":
        return _accept_off(items, analysis)
    if mode in ("light", "analysis"):
        return _accept_analysis(parent_semantic, items, analysis)
    return _accept_embedding(parent_semantic, items, analysis)
