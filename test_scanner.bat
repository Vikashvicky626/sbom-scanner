@echo off
REM Test Scanner Batch Wrapper for Windows
REM This is an alternative to the PowerShell script for users who prefer batch files

echo.
echo ================================================================
echo.
echo              SBOM Scanner Test Suite (Batch)
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

echo Running test suite...
echo.

python test_scanner.py

if errorlevel 1 (
    echo.
    echo [!] Some tests failed. See output above for details.
    pause
    exit /b 1
)

echo.
echo [OK] All tests passed!
echo.
pause

