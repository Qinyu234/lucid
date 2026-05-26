def seed_extended_algorithms(root):
    from pathlib import Path

    def w(path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding='utf-8')
    w(root / 'llm' / 'greedy_decode_fixed_vocab.py', _GREEDY)
    w(root / 'llm' / 'top_k_sample_fixed_vocab.py', _TOPK)
    w(root / 'rl' / 'epsilon_greedy_fixed_qtable.py', _EPS_GREEDY)
    w(root / 'rl' / 'q_table_bellman_update.py', _Q_UPDATE)
    w(root / 'vision' / 'sobel_edge_fixed_kernel.py', _SOBEL)
    w(root / 'vision' / 'region_mean_fixed_roi.py', _ROI_MEAN)
    w(root / 'robotics' / 'grid_astar_fixed_map.py', _ASTAR)
    w(root / 'robotics' / 'differential_drive_step.py', _DRIVE)
    w(root / 'calculus' / 'trapz_uniform_grid.py', _TRAPZ)
    w(root / 'calculus' / 'central_diff_uniform.py', _CDIFF)
    w(root / 'logic' / 'eval_bool_expr_rpn.py', _RPN)
    w(root / 'logic' / 'truth_table_fixed_inputs.py', _TRUTH)
    w(root / 'circuit' / 'simulate_logic_netlist.py', _NETLIST)
    w(root / 'info_theory' / 'entropy_discrete.py', _ENTROPY)
    w(root / 'info_theory' / 'mutual_information_discrete.py', _MI)
    w(root / 'info_theory' / 'kl_divergence_discrete.py', _KL)
    w(root / 'maxflow' / 'edmonds_karp_fixed_graph.py', _MAXFLOW)
    w(root / 'collision' / 'aabb_overlap_test.py', _AABB)
    w(root / 'collision' / 'circle_aabb_overlap.py', _CIRCLE_AABB)
