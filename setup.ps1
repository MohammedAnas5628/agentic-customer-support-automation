#requires -Version 5.1
<#!
.SYNOPSIS
    Installs and validates the ElectroMart development environment.

.DESCRIPTION
    Run this script from the repository root in PowerShell:
        .\setup.ps1

    The script creates the Python virtual environment, installs backend
    dependencies, installs frontend dependencies, and verifies the result.
    PostgreSQL creation, API keys, and database credentials remain manual.
#>

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$EnvFile = Join-Path $Backend ".env"
$Failures = [System.Collections.Generic.List[string]]::new()

function Write-Section([string]$Title) {
    Write-Host "`n=== $Title ===" -ForegroundColor Cyan
}

function Require-Command([string]$CommandName, [string]$InstallHint) {
    if (Get-Command $CommandName -ErrorAction SilentlyContinue) {
        $Version = & $CommandName --version 2>&1 | Select-Object -First 1
        Write-Host "[PASS] $CommandName $Version" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $CommandName is not installed. $InstallHint" -ForegroundColor Red
        $Failures.Add($CommandName)
    }
}

function Require-Path([string]$Path, [string]$Description) {
    if (Test-Path $Path) {
        Write-Host "[PASS] $Description" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $Description is missing: $Path" -ForegroundColor Red
        $Failures.Add($Description)
    }
}

function Run-Step([string]$Description, [scriptblock]$Action) {
    Write-Host "[RUN ] $Description" -ForegroundColor Yellow
    try {
        & $Action
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            throw "Command exited with code $LASTEXITCODE"
        }
        Write-Host "[PASS] $Description" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] ${Description}: $($_.Exception.Message)" -ForegroundColor Red
        $Failures.Add($Description)
    }
}

Set-Location $Root

Write-Section "Prerequisites"
Require-Command "python" "Install Python 3.11 or newer."
Require-Command "node" "Install Node.js 18 or newer."
Require-Command "npm.cmd" "Install Node.js; npm is included."
Require-Command "git" "Install Git for Windows."
Require-Command "psql" "Install PostgreSQL and add its bin directory to PATH."

Write-Section "Project Files"
Require-Path (Join-Path $Backend "requirements.txt") "Backend requirements"
Require-Path (Join-Path $Backend "alembic.ini") "Alembic configuration"
Require-Path (Join-Path $Frontend "package.json") "Frontend package manifest"
Require-Path (Join-Path $Frontend "next.config.ts") "Frontend Next.js configuration"

Write-Section "Python Virtual Environment"
if (-not (Test-Path $VenvPython)) {
    Run-Step "Create .venv" { & python -m venv (Join-Path $Root ".venv") }
}
Require-Path $VenvPython "Python virtual environment"

if (Test-Path $VenvPython) {
    Run-Step "Upgrade pip in .venv" { & $VenvPython -m pip install --upgrade pip }
    Run-Step "Install backend requirements" { & $VenvPython -m pip install -r (Join-Path $Backend "requirements.txt") }
}

Write-Section "Backend Dependency Verification"
$BackendModules = @(
    "fastapi", "sqlalchemy", "asyncpg", "alembic", "pgvector",
    "langchain_core", "langchain_google_genai", "langgraph",
    "pydantic_settings", "slowapi", "pwdlib"
)
foreach ($Module in $BackendModules) {
    if (Test-Path $VenvPython) {
        & $VenvPython -c "import $Module" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[PASS] Python module: $Module" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] Python module: $Module" -ForegroundColor Red
            $Failures.Add("Python module $Module")
        }
    }
}

Write-Section "Backend Environment"
if (-not (Test-Path $EnvFile)) {
    Write-Host "[WARN] backend\.env is missing. Create it before starting the backend." -ForegroundColor Yellow
    @"
GEMINI_API_KEY=replace-with-your-gemini-key
LANGSMITH_API_KEY=
LANGSMITH_TRACING=false
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/electromart
JWT_SECRET=replace-with-a-random-secret-at-least-32-characters-long
APP_ENV=development
DEBUG=true
"@ | Set-Content -Path $EnvFile -Encoding UTF8
    Write-Host "[PASS] Created backend\.env template. Fill in your values." -ForegroundColor Green
}

$EnvText = Get-Content $EnvFile -Raw
foreach ($RequiredKey in @("GEMINI_API_KEY", "DATABASE_URL", "JWT_SECRET")) {
    if ($EnvText -match "(?m)^$RequiredKey=(.+)$" -and $Matches[1].Trim()) {
        if ($RequiredKey -eq "JWT_SECRET" -and $Matches[1].Trim().Length -lt 32) {
            Write-Host "[FAIL] $RequiredKey must be at least 32 characters" -ForegroundColor Red
            $Failures.Add("$RequiredKey length")
        } else {
            Write-Host "[PASS] $RequiredKey configured" -ForegroundColor Green
        }
    } else {
        Write-Host "[FAIL] $RequiredKey is missing or empty in backend\.env" -ForegroundColor Red
        $Failures.Add("$RequiredKey configuration")
    }
}

Write-Section "Frontend Dependencies"
Push-Location $Frontend
try {
    Run-Step "Install frontend npm packages" { & npm.cmd install }
} finally {
    Pop-Location
}
Require-Path (Join-Path $Frontend "node_modules") "Frontend node_modules"

Write-Section "Database Reminder"
Write-Host "Run these commands after PostgreSQL is installed and configured:" -ForegroundColor Yellow
Write-Host '  psql -U postgres -c "CREATE DATABASE electromart;"'
Write-Host '  psql -U postgres -d electromart -c "CREATE EXTENSION IF NOT EXISTS vector;"'
if (Test-Path $VenvPython) {
    Write-Host "  .\.venv\Scripts\python.exe -m alembic -c backend\alembic.ini upgrade head"
    Write-Host "  .\.venv\Scripts\python.exe -m backend.app.rag.ingest"
}

Write-Section "Verification Commands"
if (Test-Path $VenvPython) {
    Write-Host "Backend:  .\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000"
    Write-Host "Tests:    .\.venv\Scripts\python.exe -m pytest backend\tests -q"
}
Write-Host "Frontend: cd frontend; npm.cmd run dev"
Write-Host "UI:       http://localhost:3000"
Write-Host "API:      http://localhost:8000/docs"

Write-Section "Result"
if ($Failures.Count -eq 0) {
    Write-Host "SETUP CHECK PASSED" -ForegroundColor Green
    exit 0
}

Write-Host "SETUP CHECK FAILED: $($Failures.Count) item(s) need attention" -ForegroundColor Red
$Failures | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
exit 1
