"""
Command-line interface for SBOM Scanner
"""
import sys
from pathlib import Path
import click
from colorama import init, Fore, Style

from .scanner import Scanner
from .cyclonedx_generator import CycloneDXGenerator
from . import __version__

# Initialize colorama for Windows support
init(autoreset=True)


@click.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option(
    '--output', '-o',
    type=click.Path(),
    default='sbom.json',
    help='Output file path (default: sbom.json)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['json', 'xml'], case_sensitive=False),
    default='json',
    help='Output format: json or xml (default: json)'
)
@click.option(
    '--project-name', '-n',
    type=str,
    help='Project name (defaults to directory name)'
)
@click.option(
    '--project-version', '-v',
    type=str,
    help='Project version (defaults to 1.0.0)'
)
@click.option(
    '--min-confidence',
    type=float,
    default=0.8,
    help='Minimum confidence threshold (0.0-1.0) to reduce false positives (default: 0.8)'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose output'
)
@click.option(
    '--version',
    is_flag=True,
    help='Show version and exit'
)
def main(path, output, format, project_name, project_version, min_confidence, verbose, version):
    """
    SBOM Scanner - Multi-language dependency scanner
    
    Scans projects for dependencies across multiple programming languages
    and generates a CycloneDX format SBOM with minimal false positives.
    
    Supported languages:
    - JavaScript/TypeScript (npm, yarn, pnpm)
    - Python (pip, poetry, pipenv)
    - Java (Maven, Gradle)
    - PHP (Composer)
    - .NET (NuGet)
    - Ruby (Gem)
    - Rust (Cargo)
    - Go (go modules)
    
    Examples:
    
      # Scan current directory
      sbom-scan
      
      # Scan specific directory with custom output
      sbom-scan /path/to/project -o output.json
      
      # Generate XML format with project metadata
      sbom-scan -f xml -n MyProject -v 2.1.0
      
      # Increase confidence threshold to reduce false positives
      sbom-scan --min-confidence 0.9
    """
    
    if version:
        click.echo(f"SBOM Scanner v{__version__}")
        sys.exit(0)
    
    # Print banner
    print_banner()
    
    # Validate min_confidence
    if not 0.0 <= min_confidence <= 1.0:
        click.echo(f"{Fore.RED}✗ Error: min-confidence must be between 0.0 and 1.0{Style.RESET_ALL}")
        sys.exit(1)
    
    try:
        # Initialize scanner
        scanner = Scanner(min_confidence=min_confidence)
        
        # Run scan
        click.echo(f"\n{Fore.CYAN}Starting scan...{Style.RESET_ALL}\n")
        scan_result = scanner.scan(
            path=path,
            project_name=project_name,
            project_version=project_version
        )
        
        # Check for errors
        if scan_result.errors:
            click.echo(f"\n{Fore.YELLOW}⚠ Warnings during scan:{Style.RESET_ALL}")
            for error in scan_result.errors:
                click.echo(f"  {error}")
        
        # Generate CycloneDX BOM
        click.echo(f"\n{Fore.CYAN}Generating CycloneDX BOM...{Style.RESET_ALL}")
        generator = CycloneDXGenerator()
        generator.save_to_file(scan_result, output, format)
        
        # Print summary
        print_summary(scan_result, output, format)
        
        click.echo(f"\n{Fore.GREEN}[OK] Scan completed successfully!{Style.RESET_ALL}")
        
    except FileNotFoundError as e:
        click.echo(f"{Fore.RED}[X] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except ValueError as e:
        click.echo(f"{Fore.RED}[X] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}[X] Unexpected error: {e}{Style.RESET_ALL}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}===============================================================
                                                           
              {Fore.WHITE}SBOM Scanner v{__version__}{Fore.CYAN}                        
         {Fore.WHITE}Multi-Language Dependency Scanner{Fore.CYAN}                 
                                                           
==============================================================={Style.RESET_ALL}
"""
    click.echo(banner)


def print_summary(scan_result, output_path, output_format):
    """Print scan summary"""
    # Count dependencies by ecosystem
    ecosystem_counts = {}
    for dep in scan_result.dependencies:
        ecosystem = dep.ecosystem.value
        ecosystem_counts[ecosystem] = ecosystem_counts.get(ecosystem, 0) + 1
    
    click.echo(f"\n{Fore.CYAN}=== Scan Summary ==={Style.RESET_ALL}")
    click.echo(f"Project Name:     {Fore.WHITE}{scan_result.project_name}{Style.RESET_ALL}")
    click.echo(f"Project Version:  {Fore.WHITE}{scan_result.project_version}{Style.RESET_ALL}")
    click.echo(f"Total Dependencies: {Fore.WHITE}{len(scan_result.dependencies)}{Style.RESET_ALL}")
    
    if ecosystem_counts:
        click.echo(f"\n{Fore.CYAN}Dependencies by Ecosystem:{Style.RESET_ALL}")
        for ecosystem, count in sorted(ecosystem_counts.items()):
            click.echo(f"  {Fore.WHITE}{ecosystem:12s}{Style.RESET_ALL}: {count}")
    
    click.echo(f"\n{Fore.CYAN}Output:{Style.RESET_ALL}")
    click.echo(f"  Format: {Fore.WHITE}{output_format.upper()}{Style.RESET_ALL}")
    click.echo(f"  File:   {Fore.WHITE}{output_path}{Style.RESET_ALL}")


if __name__ == '__main__':
    main()

