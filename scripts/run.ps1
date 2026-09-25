Write-Host "Starting EnterpriseFlow AI Step 2..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    py -3.12 -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r backend\requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
}

    uvicorn backend.app.main:app --reload
