# Windows Setup Guide for SBOM Scanner

This guide provides Windows-specific instructions for installing and running the SBOM Scanner on Windows using PowerShell.

## Prerequisites

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **PowerShell**
   - Windows 10/11 comes with PowerShell pre-installed
   - Open PowerShell as Administrator for installation

## Installation

### Option 1: Using PowerShell Script (Recommended)

1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd D:\Projects\SBOM
   ```

2. Run the installation script:
   ```powershell
   .\install.ps1
   ```

   If you get an error about execution policy, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Option 2: Manual Installation

1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd D:\Projects\SBOM
   ```

2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Install the package:
   ```powershell
   python -m pip install -e .
   ```

4. Verify installation:
   ```powershell
   sbom-scan --version
   ```

## Running the Scanner

### Method 1: Using the Quick Run Script (Easiest)

```powershell
# Scan current directory
.\run_sbom_scan.ps1

# Scan specific directory
.\run_sbom_scan.ps1 C:\Projects\MyApp

# Generate XML format
.\run_sbom_scan.ps1 -Format xml -Output sbom.xml

# Scan with project metadata
.\run_sbom_scan.ps1 -ProjectName "MyApp" -ProjectVersion "1.0.0"

# Show help
.\run_sbom_scan.ps1 -Help
```

### Method 2: Using the sbom-scan Command

If the `sbom-scan` command is available in your PATH:

```powershell
# Scan current directory
sbom-scan

# Scan with options
sbom-scan . -o output.json -f json

# Scan with project metadata
sbom-scan . -n "MyProject" -v "1.0.0"

# Show help
sbom-scan --help
```

### Method 3: Using Python Module Directly

If the `sbom-scan` command is not found:

```powershell
# Scan current directory
python -m sbom_scanner.cli .

# Scan with options
python -m sbom_scanner.cli . --output output.json --format json

# Show help
python -m sbom_scanner.cli --help
```

## Testing

### Run Tests Using PowerShell Script

```powershell
.\test_scanner.ps1
```

### Run Tests Using Python

```powershell
python test_scanner.py
```

## Examples

### Run Example Usage

```powershell
# Using PowerShell script
.\examples\example_usage.ps1

# Using Python directly
python examples\example_usage.py
```

## Common Issues and Solutions

### Issue: "Cannot run scripts on this system"

**Solution:** Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Python not found"

**Solution:** 
1. Install Python from https://www.python.org/downloads/
2. Make sure "Add Python to PATH" is checked during installation
3. Restart PowerShell after installation

### Issue: "'sbom-scan' is not recognized"

**Solution:** 
1. Use the Python module directly:
   ```powershell
   python -m sbom_scanner.cli .
   ```
2. Or add Python Scripts folder to PATH:
   ```powershell
   $env:PATH += ";$env:APPDATA\Python\Python3X\Scripts"
   ```

### Issue: "Module not found" errors

**Solution:** Make sure dependencies are installed:
```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Directory Structure

```
D:\Projects\SBOM\
│
├── install.ps1              # Windows installation script
├── run_sbom_scan.ps1        # Quick run script for Windows
├── test_scanner.ps1         # Test script for Windows
│
├── examples\
│   ├── example_usage.ps1    # Example usage script for Windows
│   └── example_usage.py     # Example usage Python script
│
├── sbom_scanner\            # Main package
│   ├── cli.py               # Command-line interface
│   ├── scanner.py           # Core scanner
│   └── detectors\           # Language detectors
│
└── requirements.txt         # Python dependencies
```

## PowerShell Scripts Available

1. **install.ps1** - Installs the SBOM Scanner and dependencies
2. **run_sbom_scan.ps1** - Quick run script with parameters
3. **test_scanner.ps1** - Runs the test suite
4. **examples/example_usage.ps1** - Demonstrates programmatic usage

## Next Steps

1. **Quick Start:**
   ```powershell
   .\run_sbom_scan.ps1
   ```

2. **Read Documentation:**
   - `README.md` - Full documentation
   - `QUICKSTART.md` - 5-minute quick start
   - `USAGE.md` - Detailed usage guide

3. **Run Tests:**
   ```powershell
   .\test_scanner.ps1
   ```

4. **Scan Your Project:**
   ```powershell
   .\run_sbom_scan.ps1 C:\Path\To\Your\Project
   ```

## Support

For more information and support:
- Check the main README.md
- Review QUICKSTART.md for quick examples
- See USAGE.md for detailed usage instructions
- Visit the project repository for issues and updates

## Tips for Windows Users

1. **Use PowerShell**, not Command Prompt (cmd.exe)
2. **Run as Administrator** when installing system-wide packages
3. **Use forward slashes or double backslashes** in paths:
   - Good: `C:/Projects/MyApp` or `C:\\Projects\\MyApp`
   - Avoid: `C:\Projects\MyApp` (in strings)
4. **Check execution policy** if scripts don't run
5. **Use Tab completion** for file paths in PowerShell
6. **Use .ps1 scripts** provided for better Windows integration

