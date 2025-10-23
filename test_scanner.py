#!/usr/bin/env python3
"""
Test script to verify SBOM Scanner functionality
Run this to test the scanner without installing it
"""
import sys
import os

# Add the current directory to Python path so we can import sbom_scanner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sbom_scanner.scanner import Scanner
from sbom_scanner.cyclonedx_generator import CycloneDXGenerator
from sbom_scanner.models import Ecosystem


def test_example_project():
    """Test scanning the example multi-language project"""
    print("=" * 60)
    print("Testing SBOM Scanner on Example Project")
    print("=" * 60)
    
    example_path = os.path.join(os.path.dirname(__file__), "examples", "multi_language_project")
    
    if not os.path.exists(example_path):
        print(f"❌ Example project not found at: {example_path}")
        return False
    
    print(f"\n📁 Scanning: {example_path}")
    
    # Initialize scanner
    scanner = Scanner(min_confidence=0.8)
    
    # Scan project
    try:
        result = scanner.scan(
            path=example_path,
            project_name="ExampleMultiLanguageProject",
            project_version="1.0.0"
        )
        
        print(f"\n✅ Scan completed successfully!")
        print(f"   Total dependencies found: {len(result.dependencies)}")
        
        # Count by ecosystem
        ecosystem_counts = {}
        for dep in result.dependencies:
            eco = dep.ecosystem.value
            ecosystem_counts[eco] = ecosystem_counts.get(eco, 0) + 1
        
        print(f"\n📊 Dependencies by ecosystem:")
        for eco, count in sorted(ecosystem_counts.items()):
            print(f"   {eco:12s}: {count}")
        
        # Show sample dependencies
        print(f"\n📦 Sample dependencies:")
        for i, dep in enumerate(list(result.dependencies)[:10], 1):
            print(f"   {i:2d}. {dep.name:30s} {dep.version:15s} ({dep.ecosystem.value})")
        
        if len(result.dependencies) > 10:
            print(f"   ... and {len(result.dependencies) - 10} more")
        
        # Generate CycloneDX
        print(f"\n🔄 Generating CycloneDX BOM...")
        generator = CycloneDXGenerator()
        
        # Generate JSON
        json_output = "test-output.json"
        generator.save_to_file(result, json_output, "json")
        print(f"   ✅ JSON BOM saved to: {json_output}")
        
        # Generate XML
        xml_output = "test-output.xml"
        generator.save_to_file(result, xml_output, "xml")
        print(f"   ✅ XML BOM saved to: {xml_output}")
        
        # Verify expected dependencies
        print(f"\n✅ Verification:")
        expected_packages = {
            "express": Ecosystem.NPM,
            "lodash": Ecosystem.NPM,
            "requests": Ecosystem.PYPI,
            "flask": Ecosystem.PYPI,
            "org.springframework.boot:spring-boot-starter-web": Ecosystem.MAVEN,
            "github.com/gin-gonic/gin": Ecosystem.GO,
        }
        
        found_count = 0
        for pkg_name, expected_eco in expected_packages.items():
            found = any(
                dep.name == pkg_name and dep.ecosystem == expected_eco
                for dep in result.dependencies
            )
            if found:
                print(f"   ✓ Found {pkg_name} ({expected_eco.value})")
                found_count += 1
            else:
                print(f"   ✗ Missing {pkg_name} ({expected_eco.value})")
        
        print(f"\n📈 Test Results: {found_count}/{len(expected_packages)} expected packages found")
        
        if found_count >= len(expected_packages) * 0.8:  # 80% threshold
            print(f"\n🎉 SUCCESS! Scanner is working correctly!")
            return True
        else:
            print(f"\n⚠️  WARNING: Some expected packages were not found")
            return False
    
    except Exception as e:
        print(f"\n❌ Error during scan: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detectors():
    """Test that all detectors are properly imported"""
    print("\n" + "=" * 60)
    print("Testing Detector Imports")
    print("=" * 60)
    
    try:
        from sbom_scanner.detectors import (
            NpmDetector,
            PythonDetector,
            MavenDetector,
            GradleDetector,
            ComposerDetector,
            NuGetDetector,
            RubyDetector,
            RustDetector,
            GoDetector,
        )
        
        detectors = [
            ("NPM", NpmDetector),
            ("Python", PythonDetector),
            ("Maven", MavenDetector),
            ("Gradle", GradleDetector),
            ("Composer", ComposerDetector),
            ("NuGet", NuGetDetector),
            ("Ruby", RubyDetector),
            ("Rust", RustDetector),
            ("Go", GoDetector),
        ]
        
        print(f"\n✅ All detectors imported successfully:")
        for name, detector_class in detectors:
            detector = detector_class()
            manifest_files = detector.get_manifest_files()
            print(f"   ✓ {name:12s} - Looks for: {', '.join(manifest_files)}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error importing detectors: {e}")
        return False


def test_cli():
    """Test CLI is working"""
    print("\n" + "=" * 60)
    print("Testing CLI")
    print("=" * 60)
    
    try:
        from sbom_scanner.cli import main
        from sbom_scanner import __version__
        
        print(f"\n✅ CLI imported successfully")
        print(f"   Version: {__version__}")
        print(f"   Command: sbom-scan")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error importing CLI: {e}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║              SBOM Scanner Test Suite                    ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Test 1: Detector imports
    results.append(("Detector Imports", test_detectors()))
    
    # Test 2: CLI
    results.append(("CLI", test_cli()))
    
    # Test 3: Example project scan
    results.append(("Example Project Scan", test_example_project()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print(f"\n🎉 All tests passed! SBOM Scanner is ready to use!")
        print(f"\nNext steps:")
        print(f"   1. Install: pip install -e .")
        print(f"   2. Run: sbom-scan --help")
        print(f"   3. Scan: sbom-scan .")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

