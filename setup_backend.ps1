# AudioArchitect Backend Setup Script
Write-Host "🎵 AudioArchitect - Creating Backend Files..." -ForegroundColor Cyan

# Create __init__.py files (makes Python packages)
@(
    "backend\__init__.py",
    "backend\api\__init__.py",
    "backend\api\routes\__init__.py",
    "backend\adapters\__init__.py",
    "backend\features\__init__.py",
    "backend\core\__init__.py"
) | ForEach-Object {
    New-Item -Path $_ -ItemType File -Force | Out-Null
    Write-Host "✅ Created: $_" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Backend structure ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Copy the Python code files I provided into backend/" -ForegroundColor White
Write-Host "2. Run: pip install -r backend\requirements.txt" -ForegroundColor White
Write-Host "3. Run: python -m backend.run" -ForegroundColor White
