def shared_usage_guide_util() -> str:
    """Semantic guide for generated-project leaves (not a file list)."""

    return """
src.shared is the only import surface for business leaves. Pick a category by intent:

logging — observability
  Use when: you need a logger, structured events, or run/session setup.
  Pattern: read or write ctx["meta"] (logger name, run id); never embed business rules.
  Avoid: persisting business conclusions; use validate/error_util for failure shape.

validate — data shape and IO contracts
  Use when: checking ctx["data"] types, required keys, or normalizing io.in/io.out field lists.
  Pattern: call validate helpers early; set ctx["error"] to a string or {"message": ...} on failure.
  Avoid: domain algorithms; only schema/shape work belongs here.

lib — stateless utilities
  Use when: time, ids, JSON helpers, or other pure transforms with no IO contract.
  Pattern: pass primitives or small dicts; return values to assign into ctx["data"] or ctx["meta"].
  Avoid: reading job tree, pipeline config, or files outside the project io/ area.

io — project io/ paths and files
  Use when: resolving paths under <project>/io/ or reading/writing allowed files there.
  Pattern: set meta["io_root"] via path helper, then read/write relative paths from ctx["data"].
  Avoid: tree/ snapshots, compiler output paths, or any path outside io/.

debug — development switches
  Use when: toggling debug flags or lightweight probes stored in ctx["meta"] or ctx["state"].
  Avoid: using debug helpers as permanent logging (use logging instead).

Import form: from src.shared.<category>.<module> import <module>
Function name always equals the module stem. One top-level function per file.
""".strip()
