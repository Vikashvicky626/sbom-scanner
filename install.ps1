# SBOM Scanner Installation Script for Windows PowerShell

Write-Host "╔══════════════════════════════════════════════════════════╗"
Write-Host "║                                                          ║"
Write-Host "║           SBOM Scanner Installation Script              ║"
Write-Host "║                                                          ║"
Write-Host "╚══════════════════════════════════════════════════════════╝"
Write-Host ""

# Check Python
Write-Host "Checking Python version..."
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✓ Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/"
    exit 1
}

# Check pip
Write-Host "Checking pip..."
try {
    $pipVersion = & pip --version 2>&1
    Write-Host "✓ Found pip" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Please install pip." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..."
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install package
Write-Host ""
Write-Host "Installing SBOM Scanner..."
pip install -e .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install SBOM Scanner" -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..."
try {
    $version = & sbom-scan --version 2>&1
    Write-Host "✓ SBOM Scanner installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host $version
} catch {
    Write-Host "⚠️  Command 'sbom-scan' not found in PATH" -ForegroundColor Yellow
    Write-Host "   You can run: python -m sbom_scanner.cli"
}

# Run tests
Write-Host ""
Write-Host "Running tests..."
python test_scanner.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠️  Some tests failed, but installation may still work" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗"
Write-Host "║                                                          ║"
Write-Host "║              Installation Complete! 🎉                   ║"
Write-Host "║                                                          ║"
Write-Host "╚══════════════════════════════════════════════════════════╝"
Write-Host ""
Write-Host "Quick Start:"
Write-Host "  sbom-scan --help"
Write-Host "  sbom-scan ."
Write-Host ""
Write-Host "Documentation:"
Write-Host "  README.md      - Full documentation"
Write-Host "  QUICKSTART.md  - Get started in 5 minutes"
Write-Host "  USAGE.md       - Detailed usage guide"
Write-Host ""

