@echo off
REM Quick Run Script for SBOM Scanner on Windows (Batch File)
REM This is an alternative to the PowerShell script for users who prefer batch files

echo.
echo ================================================================
echo.
echo              SBOM Scanner - Quick Run (Batch)
echo.
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found. Please install Python 3.8 or higher.
    echo     Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if sbom-scan command is available
sbom-scan --version >nul 2>&1
if errorlevel 1 (
    echo Running via Python module...
    echo.
    python -m sbom_scanner.cli %*
) else (
    echo Running sbom-scan command...
    echo.
    sbom-scan %*
)

if errorlevel 1 (
    echo.
    echo [X] Scan failed. See output above for details.
    pause
    exit /b 1
)

echo.
echo [OK] Scan completed successfully!
echo.
pause

