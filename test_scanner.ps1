# Test Scanner PowerShell Wrapper for Windows
# Run this script to test the SBOM Scanner on Windows

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║              SBOM Scanner Test Suite                    ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✓ Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to script directory
Push-Location $scriptDir

try {
    # Run the Python test script
    Write-Host "Running test suite..." -ForegroundColor Cyan
    Write-Host ""
    
    python test_scanner.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️  Some tests failed. See output above for details." -ForegroundColor Yellow
    }
} finally {
    # Return to original directory
    Pop-Location
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

