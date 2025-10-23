# Quick Run Script for SBOM Scanner on Windows
# This script runs the SBOM scanner on the current directory

param(
    [Parameter(Position=0)]
    [string]$Path = ".",
    
    [Parameter()]
    [string]$Output = "sbom.json",
    
    [Parameter()]
    [ValidateSet("json", "xml")]
    [string]$Format = "json",
    
    [Parameter()]
    [string]$ProjectName,
    
    [Parameter()]
    [string]$ProjectVersion,
    
    [Parameter()]
    [double]$MinConfidence = 0.8,
    
    [switch]$Verbose,
    
    [switch]$Help
)

# Show help
if ($Help) {
    Write-Host ""
    Write-Host "SBOM Scanner - Quick Run Script for Windows" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\run_sbom_scan.ps1 [Path] [Options]"
    Write-Host ""
    Write-Host "PARAMETERS:" -ForegroundColor Yellow
    Write-Host "  -Path <path>              Path to scan (default: current directory)"
    Write-Host "  -Output <file>            Output file path (default: sbom.json)"
    Write-Host "  -Format <json|xml>        Output format (default: json)"
    Write-Host "  -ProjectName <name>       Project name"
    Write-Host "  -ProjectVersion <version> Project version"
    Write-Host "  -MinConfidence <0.0-1.0>  Minimum confidence threshold (default: 0.8)"
    Write-Host "  -Verbose                  Enable verbose output"
    Write-Host "  -Help                     Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  # Scan current directory"
    Write-Host "  .\run_sbom_scan.ps1"
    Write-Host ""
    Write-Host "  # Scan specific directory"
    Write-Host "  .\run_sbom_scan.ps1 C:\Projects\MyApp"
    Write-Host ""
    Write-Host "  # Generate XML format with project info"
    Write-Host "  .\run_sbom_scan.ps1 -Format xml -ProjectName MyApp -ProjectVersion 1.0.0"
    Write-Host ""
    Write-Host "  # Scan with higher confidence threshold"
    Write-Host "  .\run_sbom_scan.ps1 -MinConfidence 0.9"
    Write-Host ""
    exit 0
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║              SBOM Scanner - Quick Run                    ║" -ForegroundColor Cyan
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

# Build command arguments
$args = @()
$args += $Path

if ($Output) {
    $args += "--output"
    $args += $Output
}

if ($Format) {
    $args += "--format"
    $args += $Format
}

if ($ProjectName) {
    $args += "--project-name"
    $args += $ProjectName
}

if ($ProjectVersion) {
    $args += "--project-version"
    $args += $ProjectVersion
}

if ($MinConfidence) {
    $args += "--min-confidence"
    $args += $MinConfidence
}

if ($Verbose) {
    $args += "--verbose"
}

# Check if sbom-scan command is available
Write-Host ""
Write-Host "Checking SBOM Scanner installation..." -ForegroundColor Cyan

$commandExists = $false
try {
    $null = & sbom-scan --version 2>&1
    $commandExists = $true
} catch {
    $commandExists = $false
}

if ($commandExists) {
    Write-Host "✓ Running sbom-scan command..." -ForegroundColor Green
    Write-Host ""
    & sbom-scan @args
} else {
    Write-Host "⚠️  'sbom-scan' command not found. Running via Python module..." -ForegroundColor Yellow
    Write-Host ""
    & python -m sbom_scanner.cli @args
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Scan completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Output saved to: $Output" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Scan failed. See output above for details." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""

