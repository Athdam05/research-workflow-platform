# Research Workflow & Insight Intelligence Platform — Backend

A hackathon-ready Flask + SQLite REST API for managing research projects,
papers, experiments, insights, and relationship graphs.

---

## Quick Start

```bash
# 1. Clone / navigate to the backend folder
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python app.py
```

The server starts at **http://localhost:5000**

---

## Folder Structure

```
backend/
├── app.py                  ← Flask app factory & entry point
├── database.py             ← SQLAlchemy init + table creation
├── requirements.txt
├── research.db             ← SQLite file (auto-created on first run)
├── uploads/                ← Uploaded paper files stored here
│
├── models/
│   ├── project_model.py
│   ├── paper_model.py
│   ├── experiment_model.py
│   ├── insight_model.py
│   └── relationship_model.py
│
├── routes/
│   ├── project_routes.py
│   ├── paper_routes.py
│   ├── experiment_routes.py
│   ├── insight_routes.py
│   └── relationship_routes.py
│
└── utils/
    └── file_upload.py
```

---

## API Reference

### Health Check

```
GET /api/health
```

---

### 1 · Projects `/api/projects`

| Method | URL               | Action               |
| ------ | ----------------- | -------------------- |
| GET    | /api/projects     | List all             |
| POST   | /api/projects     | Create               |
| GET    | /api/projects/:id | Get one (+ children) |
| PUT    | /api/projects/:id | Update               |
| DELETE | /api/projects/:id | Delete (cascade)     |

---

### 2 · Papers `/api/papers`

| Method | URL                     | Action                 |
| ------ | ----------------------- | ---------------------- |
| GET    | /api/papers?project_id= | List (filtered)        |
| POST   | /api/papers             | Create / upload        |
| GET    | /api/papers/:id         | Get one                |
| PUT    | /api/papers/:id         | Update / add AI fields |
| DELETE | /api/papers/:id         | Delete                 |

---

### 3 · Experiments `/api/experiments`

| Method | URL                          | Action  |
| ------ | ---------------------------- | ------- |
| GET    | /api/experiments?project_id= | List    |
| POST   | /api/experiments             | Create  |
| GET    | /api/experiments/:id         | Get one |
| PUT    | /api/experiments/:id         | Update  |
| DELETE | /api/experiments/:id         | Delete  |

---

### 4 · Insights `/api/insights`

| Method | URL                       | Action  |
| ------ | ------------------------- | ------- |
| GET    | /api/insights?project_id= | List    |
| POST   | /api/insights             | Create  |
| GET    | /api/insights/:id         | Get one |
| PUT    | /api/insights/:id         | Update  |
| DELETE | /api/insights/:id         | Delete  |

---

### 5 · Relationships `/api/relationships`

| Method | URL                                  | Action          |
| ------ | ------------------------------------ | --------------- |
| GET    | /api/relationships                   | List (filtered) |
| POST   | /api/relationships                   | Create edge     |
| GET    | /api/relationships/:id               | Get one         |
| DELETE | /api/relationships/:id               | Delete          |
| GET    | /api/relationships/graph?project_id= | Full graph      |

---

## curl Test Examples

### Health check

```bash
curl http://localhost:5000/api/health
```

---

### Projects

```bash
# Create a project
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"title": "LLM Reasoning Study", "description": "Exploring chain-of-thought prompting"}'

# List all projects
curl http://localhost:5000/api/projects

# Get project 1 with all children
curl http://localhost:5000/api/projects/1

# Update project
curl -X PUT http://localhost:5000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'

# Delete project
curl -X DELETE http://localhost:5000/api/projects/1
```

---

### Papers

```bash
# Add a paper by external link
curl -X POST http://localhost:5000/api/papers \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "title": "Chain-of-Thought Prompting Elicits Reasoning in LLMs",
    "link": "https://arxiv.org/abs/2201.11903",
    "tags": "LLM,reasoning,prompting",
    "summary": "Demonstrates that CoT prompting improves reasoning benchmarks."
  }'

# Upload a paper PDF
curl -X POST http://localhost:5000/api/papers \
  -F "project_id=1" \
  -F "title=My Paper" \
  -F "file=@/path/to/paper.pdf"

# List papers for project 1
curl "http://localhost:5000/api/papers?project_id=1"

# Store AI-generated summary + keywords (PUT)
curl -X PUT http://localhost:5000/api/papers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "AI-generated summary here...",
    "keywords": "transformer,attention,scaling",
    "concepts": "in-context learning,emergence,few-shot"
  }'
```

---

### Experiments

```bash
# Create an experiment
curl -X POST http://localhost:5000/api/experiments \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "title": "CoT vs Standard Prompting on GSM8K",
    "hypothesis": "CoT prompting will outperform standard prompting by >10%.",
    "method": "Evaluate GPT-4 on GSM8K with/without CoT. 500 samples each.",
    "result": "CoT: 92% accuracy. Standard: 78% accuracy. Hypothesis confirmed.",
    "related_paper_id": 1
  }'

# Update results after running
curl -X PUT http://localhost:5000/api/experiments/1 \
  -H "Content-Type: application/json" \
  -d '{"result": "Final result: CoT improved accuracy by 14 percentage points."}'
```

---

### Insights

```bash
# Add an insight linked to a paper and experiment
curl -X POST http://localhost:5000/api/insights \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "content": "CoT benefits appear to scale with model size — smaller models show no gain.",
    "related_paper_id": 1,
    "related_experiment_id": 1
  }'

# List insights for project 1
curl "http://localhost:5000/api/insights?project_id=1"
```

---

### Relationships

```bash
# Link a paper → experiment
curl -X POST http://localhost:5000/api/relationships \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "paper",
    "source_id": 1,
    "target_type": "experiment",
    "target_id": 1,
    "label": "motivates"
  }'

# Link an experiment → insight
curl -X POST http://localhost:5000/api/relationships \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "experiment",
    "source_id": 1,
    "target_type": "insight",
    "target_id": 1,
    "label": "produces"
  }'

# Get the full graph for project 1
curl "http://localhost:5000/api/relationships/graph?project_id=1"
```

---

## Example JSON Responses

### Project (detail)

```json
{
  "id": 1,
  "title": "LLM Reasoning Study",
  "description": "Exploring chain-of-thought prompting",
  "created_at": "2024-11-01T10:00:00",
  "paper_count": 1,
  "experiment_count": 1,
  "insight_count": 1,
  "papers": [...],
  "experiments": [...],
  "insights": [...]
}
```

### Paper

```json
{
  "id": 1,
  "project_id": 1,
  "title": "Chain-of-Thought Prompting Elicits Reasoning in LLMs",
  "file_path": null,
  "link": "https://arxiv.org/abs/2201.11903",
  "tags": ["LLM", "reasoning", "prompting"],
  "summary": "Demonstrates that CoT prompting improves reasoning benchmarks.",
  "keywords": ["transformer", "attention", "scaling"],
  "concepts": ["in-context learning", "emergence", "few-shot"],
  "created_at": "2024-11-01T10:05:00"
}
```

### Graph response

```json
{
  "nodes": [
    {
      "id": "paper_1",
      "type": "paper",
      "label": "Chain-of-Thought Prompting..."
    },
    {
      "id": "experiment_1",
      "type": "experiment",
      "label": "CoT vs Standard Prompting"
    },
    {
      "id": "insight_1",
      "type": "insight",
      "label": "CoT benefits appear to scale..."
    }
  ],
  "edges": [
    {
      "id": 1,
      "source_type": "paper",
      "source_id": 1,
      "target_type": "experiment",
      "target_id": 1,
      "label": "motivates"
    },
    {
      "id": 2,
      "source_type": "experiment",
      "source_id": 1,
      "target_type": "insight",
      "target_id": 1,
      "label": "produces"
    }
  ]
}
```

---

## AI Integration Guide

The backend has three AI-ready fields on every paper:

| Field      | Purpose                             | How to populate       |
| ---------- | ----------------------------------- | --------------------- |
| `summary`  | Plain-English paper summary         | `PUT /api/papers/:id` |
| `keywords` | Comma-separated extracted keywords  | `PUT /api/papers/:id` |
| `concepts` | Comma-separated high-level concepts | `PUT /api/papers/:id` |

Your AI service reads the paper (by `file_path` or `link`), generates the values,
then calls `PUT /api/papers/:id` to store them. No other changes are needed.

---

## Notes

- The SQLite database (`research.db`) is auto-created on first run.
- Uploaded files land in `backend/uploads/` and are referenced by relative path.
- CORS is open (`*`) for hackathon convenience — lock it down before any public deployment.
- All timestamps are UTC ISO-8601 strings.
