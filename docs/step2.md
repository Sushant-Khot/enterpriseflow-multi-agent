# Step 2 — Project Foundation

## Objective

Build a zero-cost local foundation before connecting paid/usage-based AWS components.

## Completed components

### 1. FastAPI
The API layer is implemented in `backend/app/main.py` and `backend/app/api/routes.py`.

### 2. Configuration
`pydantic-settings` loads configuration from `.env`.

### 3. LangGraph
`backend/app/graph/workflow.py` defines the initial graph:

START
-> security_gate
-> orchestrator
-> A1/A2/A3/A4
-> END

### 4. Shared state
`backend/app/graph/state.py` defines the state contract.

### 5. Orchestrator
Step 2 uses a deterministic keyword router. This avoids unnecessary Bedrock calls during development.

### 6. Workflow store
An in-memory store is used temporarily. It will later be replaced by DynamoDB.

### 7. Docker
The complete backend can be built as a Docker image.

## Deliberate Step 2 limitations

The following are placeholders and are intentionally not implemented yet:

- Amazon Bedrock calls
- PII detection
- prompt-injection detection
- production RBAC
- DynamoDB persistence
- S3 integration
- EventBridge
- Lambda
- SQS
- CloudWatch integration
- human approval UI
- specialist agent business logic
- React frontend

These are later phases. Keeping them out of Step 2 makes local testing cheap and isolates failures.

## Acceptance criteria

Run:

```powershell
pytest -q
```

All tests should pass.

Then:

```powershell
uvicorn backend.app.main:app --reload
```

and verify:

```text
GET  /api/v1/health
POST /api/v1/chat
GET  /api/v1/workflows/{workflow_id}
```
