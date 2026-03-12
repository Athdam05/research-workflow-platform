# test_api.py
# Run with: python test_api.py
# Tests every single API endpoint and prints pass/fail results.

import requests
import json
import sys

BASE = "http://127.0.0.1:5000/api"
PASS = "✅"
FAIL = "❌"
results = {"passed": 0, "failed": 0}


def check(label, response, expected_status, check_fn=None):
    ok = response.status_code == expected_status
    if ok and check_fn:
        ok = check_fn(response.json())
    status = PASS if ok else FAIL
    if ok:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print(f"  {status} FAIL — {label}")
        print(f"       Status: {response.status_code} (expected {expected_status})")
        try:
            print(f"       Body:   {response.json()}")
        except Exception:
            print(f"       Body:   {response.text}")
        return None
    print(f"  {status}  {label}")
    return response.json()


def section(title):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")


# ── Health ────────────────────────────────────────────────────────────────────
section("HEALTH CHECK")
check("GET /api/health", requests.get(f"{BASE}/health"), 200,
      lambda r: r["status"] == "ok")

# ── Projects ──────────────────────────────────────────────────────────────────
section("PROJECTS")
r = check("POST /api/projects — create",
          requests.post(f"{BASE}/projects", json={
              "title": "Test Project",
              "description": "Created by test script"
          }), 201, lambda r: r["title"] == "Test Project")
project_id = r["id"] if r else None

check("GET  /api/projects — list",
      requests.get(f"{BASE}/projects"), 200,
      lambda r: isinstance(r, list))

if project_id:
    check("GET  /api/projects/:id — detail",
          requests.get(f"{BASE}/projects/{project_id}"), 200,
          lambda r: r["id"] == project_id)

    check("PUT  /api/projects/:id — update",
          requests.put(f"{BASE}/projects/{project_id}",
                       json={"description": "Updated description"}), 200,
          lambda r: r["description"] == "Updated description")

check("POST /api/projects — missing title (should 400)",
      requests.post(f"{BASE}/projects", json={"description": "no title"}), 400)

# ── Papers ────────────────────────────────────────────────────────────────────
section("PAPERS")
r = check("POST /api/papers — create",
          requests.post(f"{BASE}/papers", json={
              "project_id": project_id,
              "title": "Attention Is All You Need",
              "link": "https://arxiv.org/abs/1706.03762",
              "tags": "transformer,attention,NLP",
              "summary": "Introduces the transformer architecture."
          }), 201, lambda r: r["title"] == "Attention Is All You Need")
paper_id = r["id"] if r else None

check("GET  /api/papers — list all",
      requests.get(f"{BASE}/papers"), 200,
      lambda r: isinstance(r, list))

check(f"GET  /api/papers?project_id={project_id} — filter",
      requests.get(f"{BASE}/papers?project_id={project_id}"), 200,
      lambda r: len(r) >= 1)

if paper_id:
    check("GET  /api/papers/:id — detail",
          requests.get(f"{BASE}/papers/{paper_id}"), 200,
          lambda r: r["id"] == paper_id)

    check("PUT  /api/papers/:id — store AI fields",
          requests.put(f"{BASE}/papers/{paper_id}", json={
              "summary":  "AI summary: Proposes self-attention for seq2seq tasks.",
              "keywords": "self-attention,multi-head,positional-encoding",
              "concepts": "attention mechanism,encoder-decoder,transformers"
          }), 200, lambda r: "self-attention" in r["keywords"])

check("POST /api/papers — missing project_id (should 400)",
      requests.post(f"{BASE}/papers", json={"title": "No project"}), 400)

# ── Experiments ───────────────────────────────────────────────────────────────
section("EXPERIMENTS")
r = check("POST /api/experiments — create",
          requests.post(f"{BASE}/experiments", json={
              "project_id":      project_id,
              "title":           "Transformer vs LSTM on BLEU score",
              "hypothesis":      "Transformer will outperform LSTM by >5 BLEU points.",
              "method":          "Train both models on WMT14 EN-DE. Evaluate BLEU.",
              "result":          "Transformer: 28.4 BLEU. LSTM: 23.1 BLEU. Confirmed.",
              "related_paper_id": paper_id
          }), 201)
experiment_id = r["id"] if r else None

check("GET  /api/experiments — list all",
      requests.get(f"{BASE}/experiments"), 200,
      lambda r: isinstance(r, list))

check(f"GET  /api/experiments?project_id={project_id} — filter",
      requests.get(f"{BASE}/experiments?project_id={project_id}"), 200,
      lambda r: len(r) >= 1)

if experiment_id:
    check("GET  /api/experiments/:id — detail",
          requests.get(f"{BASE}/experiments/{experiment_id}"), 200,
          lambda r: r["id"] == experiment_id)

    check("PUT  /api/experiments/:id — update result",
          requests.put(f"{BASE}/experiments/{experiment_id}",
                       json={"result": "Final: +5.3 BLEU improvement confirmed."}), 200)

# ── Insights ──────────────────────────────────────────────────────────────────
section("INSIGHTS")
r = check("POST /api/insights — create",
          requests.post(f"{BASE}/insights", json={
              "project_id":           project_id,
              "content":              "Transformer gains scale with model size. Smaller models show diminishing returns.",
              "related_paper_id":     paper_id,
              "related_experiment_id": experiment_id
          }), 201)
insight_id = r["id"] if r else None

check("GET  /api/insights — list all",
      requests.get(f"{BASE}/insights"), 200,
      lambda r: isinstance(r, list))

check(f"GET  /api/insights?project_id={project_id} — filter",
      requests.get(f"{BASE}/insights?project_id={project_id}"), 200,
      lambda r: len(r) >= 1)

if insight_id:
    check("GET  /api/insights/:id — detail",
          requests.get(f"{BASE}/insights/{insight_id}"), 200,
          lambda r: r["id"] == insight_id)

    check("PUT  /api/insights/:id — update",
          requests.put(f"{BASE}/insights/{insight_id}",
                       json={"content": "Updated: Attention heads specialise by layer depth."}), 200)

# ── Relationships ─────────────────────────────────────────────────────────────
section("RELATIONSHIPS")
r = check("POST /api/relationships — paper → experiment",
          requests.post(f"{BASE}/relationships", json={
              "source_type": "paper",
              "source_id":   paper_id,
              "target_type": "experiment",
              "target_id":   experiment_id,
              "label":       "motivates"
          }), 201)
rel_id = r["id"] if r else None

r2 = check("POST /api/relationships — experiment → insight",
           requests.post(f"{BASE}/relationships", json={
               "source_type": "experiment",
               "source_id":   experiment_id,
               "target_type": "insight",
               "target_id":   insight_id,
               "label":       "produces"
           }), 201)

check("GET  /api/relationships — list all",
      requests.get(f"{BASE}/relationships"), 200,
      lambda r: isinstance(r, list))

if rel_id:
    check("GET  /api/relationships/:id — detail",
          requests.get(f"{BASE}/relationships/{rel_id}"), 200,
          lambda r: r["id"] == rel_id)

check("POST /api/relationships — invalid type (should 400)",
      requests.post(f"{BASE}/relationships", json={
          "source_type": "invalid", "source_id": 1,
          "target_type": "paper",  "target_id": 1
      }), 400)

check(f"GET  /api/relationships/graph?project_id={project_id} — graph",
      requests.get(f"{BASE}/relationships/graph?project_id={project_id}"), 200,
      lambda r: "nodes" in r and "edges" in r)

# ── 404 handling ──────────────────────────────────────────────────────────────
section("ERROR HANDLING")
check("GET  /api/projects/99999 — not found (should 404)",
      requests.get(f"{BASE}/projects/99999"), 404)
check("GET  /api/papers/99999   — not found (should 404)",
      requests.get(f"{BASE}/papers/99999"), 404)

# ── Cleanup: delete test project (cascades to children) ───────────────────────
section("CLEANUP")
if project_id:
    check(f"DELETE /api/projects/{project_id} — cascade delete",
          requests.delete(f"{BASE}/projects/{project_id}"), 200)
    check("GET  /api/projects/:id after delete (should 404)",
          requests.get(f"{BASE}/projects/{project_id}"), 404)
if rel_id:
    # Relationships have no FK to project so must be deleted explicitly
    check(f"DELETE /api/relationships/{rel_id} — explicit delete",
          requests.delete(f"{BASE}/relationships/{rel_id}"), 200)
    check("GET  /api/relationships/:id after delete (should 404)",
          requests.get(f"{BASE}/relationships/{rel_id}"), 404)

# ── Summary ───────────────────────────────────────────────────────────────────
total = results["passed"] + results["failed"]
print(f"\n{'═'*50}")
print(f"  Results: {results['passed']}/{total} tests passed")
if results["failed"] == 0:
    print("  🎉 All tests passed! Backend is fully working.")
else:
    print(f"  ⚠️  {results['failed']} test(s) failed. Check output above.")
print(f"{'═'*50}\n")
sys.exit(0 if results["failed"] == 0 else 1)
