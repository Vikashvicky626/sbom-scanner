#!/usr/bin/env python3
"""
Example usage of SBOM Scanner programmatically
"""
from sbom_scanner.scanner import Scanner
from sbom_scanner.cyclonedx_generator import CycloneDXGenerator


def main():
    print("SBOM Scanner - Example Usage\n")
    
    # Example 1: Basic scan
    print("Example 1: Basic Scan")
    print("-" * 50)
    scanner = Scanner(min_confidence=0.8)
    result = scanner.scan(
        path=".",
        project_name="ExampleProject",
        project_version="1.0.0"
    )
    
    print(f"\nFound {len(result.dependencies)} unique dependencies")
    print("\nFirst 5 dependencies:")
    for i, dep in enumerate(list(result.dependencies)[:5], 1):
        print(f"  {i}. {dep.name}@{dep.version} ({dep.ecosystem.value})")
    
    # Example 2: Generate SBOM
    print("\n\nExample 2: Generate CycloneDX SBOM")
    print("-" * 50)
    generator = CycloneDXGenerator()
    
    # Generate JSON
    json_sbom = generator.generate(result, output_format="json")
    print(f"Generated JSON SBOM ({len(json_sbom)} characters)")
    
    # Save to file
    generator.save_to_file(result, "example-sbom.json", "json")
    
    # Example 3: Filter dependencies by ecosystem
    print("\n\nExample 3: Filter by Ecosystem")
    print("-" * 50)
    from sbom_scanner.models import Ecosystem
    
    npm_deps = [d for d in result.dependencies if d.ecosystem == Ecosystem.NPM]
    python_deps = [d for d in result.dependencies if d.ecosystem == Ecosystem.PYPI]
    
    print(f"NPM dependencies: {len(npm_deps)}")
    print(f"Python dependencies: {len(python_deps)}")
    
    # Example 4: High confidence only
    print("\n\nExample 4: High Confidence Dependencies Only")
    print("-" * 50)
    high_conf_deps = [d for d in result.dependencies if d.confidence >= 0.95]
    print(f"Dependencies with confidence >= 0.95: {len(high_conf_deps)}")
    
    for dep in high_conf_deps[:3]:
        print(f"  - {dep.name}@{dep.version} (confidence: {dep.confidence})")
    
    # Example 5: Dependencies by type
    print("\n\nExample 5: Dependencies by Type")
    print("-" * 50)
    from sbom_scanner.models import DependencyType
    
    direct_deps = [d for d in result.dependencies if d.dependency_type == DependencyType.DIRECT]
    dev_deps = [d for d in result.dependencies if d.dependency_type == DependencyType.DEV]
    
    print(f"Direct dependencies: {len(direct_deps)}")
    print(f"Dev dependencies: {len(dev_deps)}")
    
    print("\n✓ Examples completed successfully!")


if __name__ == "__main__":
    main()

