#!/bin/bash
# SBOM Scanner Installation Script for Linux/Mac

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║           SBOM Scanner Installation Script              ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Check pip
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
else
    echo "❌ pip not found. Please install pip."
    exit 1
fi
echo "✓ Found pip"

# Install dependencies
echo ""
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Install package
echo ""
echo "Installing SBOM Scanner..."
$PIP_CMD install -e .

# Verify installation
echo ""
echo "Verifying installation..."
if command -v sbom-scan &> /dev/null; then
    echo "✓ SBOM Scanner installed successfully!"
    echo ""
    sbom-scan --version
else
    echo "⚠️  Command 'sbom-scan' not found in PATH"
    echo "   You may need to add ~/.local/bin to your PATH"
    echo "   Or run: $PYTHON_CMD -m sbom_scanner.cli"
fi

# Run tests
echo ""
echo "Running tests..."
$PYTHON_CMD test_scanner.py

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              Installation Complete! 🎉                   ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Quick Start:"
echo "  sbom-scan --help"
echo "  sbom-scan ."
echo ""
echo "Documentation:"
echo "  README.md      - Full documentation"
echo "  QUICKSTART.md  - Get started in 5 minutes"
echo "  USAGE.md       - Detailed usage guide"
echo ""

