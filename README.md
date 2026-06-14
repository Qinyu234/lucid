# Lucid

> A code clarity tool built by a first-year CE student who couldn't read their own code.

**The problem:** State scattered across files, no record of who can modify it or what depends on it. Every change required mentally reconstructing the entire dependency chain just to avoid breaking something.

**The approach:** Extract the implicit access structure of every piece of state — who writes it, who reads it — and make it explicitly queryable. Reorganize the code into a clean virtual layer for editing without touching the original files.

---

## Core concepts

**Access Contract** — for every piece of state:
```json
{
  "cartTotal": {
    "defined": "CartService.ts:12",
    "write_sites": ["CartService.addItem:L34", "CartService.removeItem:L89"],
    "use_sites": ["CartSummary.tsx:L45", "CheckoutButton.tsx:L67"],
    "source": "inferred"
  }
}
```

**Virtual Files** — a projection layer over the real code. Edit here; the tool diffs and patches back. If the real files change externally, the virtual layer regenerates automatically.

---

## Architecture

```
Code → Ingestion → Graph → Analysis → Virtual Layer → Views → Generation (Phase 3)
```

| View | Question |
|------|----------|
| Def-Use Contract | Where is this assigned? Where is it read? ← MVP |
| Structure | What does the code look like? |
| Data Flow | Where does this value come from? |
| Event Flow | What happens after this fires? |
| Impact | If I change this, what breaks? |
| Test | Is this covered? Does it meet its performance budget? |

**Using existing tools:** Tree-sitter, ts-morph, dependency-cruiser, Joern, OpenTelemetry, Jest/Vitest, Lighthouse, LangGraph, VSCode Extension API.

**Building:** Virtual Files diff/patch engine, access contract inference, writers → readers impact propagation.

---

## Status

Phase 1 in progress — single file parsing, writers/readers extraction, interactive graph view.

Full thinking behind the design: [devlog →](link)

---

*Built while learning to read other people's code. Works on any codebase — frontend, backend, or otherwise.*

---

## Docs

[Full architecture document](https://htmlpreview.github.io/?https://github.com/Qinyu234/lucid/blob/main/ARCHITECTURE.html) — system layers, data structures, isolation strategy, views, roadmap. Best viewed rendered.