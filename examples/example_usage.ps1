# Example Usage PowerShell Wrapper for Windows
# Run this script to see example usage of SBOM Scanner on Windows

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║         SBOM Scanner - Example Usage                    ║" -ForegroundColor Cyan
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
$parentDir = Split-Path -Parent $scriptDir

# Change to parent directory (project root)
Push-Location $parentDir

try {
    # Run the Python example script
    Write-Host "Running example usage..." -ForegroundColor Cyan
    Write-Host ""
    
    python examples\example_usage.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Example completed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️  Example failed. See output above for details." -ForegroundColor Yellow
    }
} finally {
    # Return to original directory
    Pop-Location
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

