# Script to fix psycopg2-binary installation issue
# Run this script in PowerShell as Administrator if needed

Write-Host "Fixing psycopg2-binary installation..." -ForegroundColor Yellow

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Uninstall broken package
Write-Host "Uninstalling psycopg2-binary..." -ForegroundColor Cyan
pip uninstall psycopg2-binary -y

# Install fresh
Write-Host "Installing psycopg2-binary..." -ForegroundColor Cyan
pip install --no-cache-dir psycopg2-binary

Write-Host "Done! Try running uvicorn again." -ForegroundColor Green
