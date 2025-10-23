# Simple SBOM Scanner Installation Script

Write-Host "SBOM Scanner Installation Script"
Write-Host ""

# Check Python
Write-Host "Checking Python version..."
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install package
Write-Host "Installing SBOM Scanner..."
pip install -e .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install SBOM Scanner" -ForegroundColor Red
    exit 1
}

Write-Host "Installation Complete!"
Write-Host "Run: sbom-scan --help"
