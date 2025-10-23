"""
Core scanner that orchestrates all detectors
"""
from pathlib import Path
from typing import List, Set, Optional
from .models import ScanResult, Dependency
from .detectors import (
    BaseDetector,
    NpmDetector,
    PythonDetector,
    MavenDetector,
    GradleDetector,
    ComposerDetector,
    NuGetDetector,
    RubyDetector,
    RustDetector,
    GoDetector,
    ConanDetector,
    VcpkgDetector,
    CMakeDetector,
    PlatformIODetector,
    ArduinoDetector,
    MbedDetector,
)


class Scanner:
    """Main scanner class that coordinates all language detectors"""
    
    def __init__(self, min_confidence: float = 0.8):
        """
        Initialize scanner with all detectors
        
        Args:
            min_confidence: Minimum confidence threshold to include dependencies (0.0-1.0)
                          Higher values reduce false positives
        """
        self.min_confidence = min_confidence
        self.detectors: List[BaseDetector] = [
            NpmDetector(),
            PythonDetector(),
            MavenDetector(),
            GradleDetector(),
            ComposerDetector(),
            NuGetDetector(),
            RubyDetector(),
            RustDetector(),
            GoDetector(),
            ConanDetector(),
            VcpkgDetector(),
            CMakeDetector(),
            PlatformIODetector(),
            ArduinoDetector(),
            MbedDetector(),
        ]
    
    def scan(self, path: str, project_name: Optional[str] = None, 
             project_version: Optional[str] = None) -> ScanResult:
        """
        Scan a project directory for dependencies
        
        Args:
            path: Path to the project directory
            project_name: Optional project name (defaults to directory name)
            project_version: Optional project version (defaults to "1.0.0")
        
        Returns:
            ScanResult containing all discovered dependencies
        """
        scan_path = Path(path).resolve()
        
        if not scan_path.exists():
            raise FileNotFoundError(f"Path does not exist: {scan_path}")
        
        if not scan_path.is_dir():
            raise ValueError(f"Path is not a directory: {scan_path}")
        
        # Determine project name
        if project_name is None:
            project_name = scan_path.name
        
        # Create result object
        result = ScanResult(
            project_name=project_name,
            project_version=project_version or "1.0.0",
            scan_path=str(scan_path)
        )
        
        # Run all detectors
        print(f"Scanning project: {project_name} at {scan_path}")
        
        for detector in self.detectors:
            detector_name = detector.__class__.__name__
            
            try:
                if detector.detect(scan_path):
                    print(f"  [+] Detected {detector_name}")
                    dependencies = detector.parse(scan_path)
                    
                    # Filter by confidence threshold
                    filtered_deps = {
                        dep for dep in dependencies 
                        if dep.confidence >= self.min_confidence
                    }
                    
                    if filtered_deps:
                        print(f"    Found {len(filtered_deps)} dependencies")
                        for dep in filtered_deps:
                            result.add_dependency(dep)
                    else:
                        print(f"    No dependencies found (after confidence filtering)")
            
            except Exception as e:
                error_msg = f"Error in {detector_name}: {str(e)}"
                print(f"  [X] {error_msg}")
                result.add_error(error_msg)
        
        # Remove duplicates and apply additional false positive reduction
        result.dependencies = self._reduce_false_positives(result.dependencies)
        
        print(f"\nTotal unique dependencies found: {len(result.dependencies)}")
        
        return result
    
    def _reduce_false_positives(self, dependencies: Set[Dependency]) -> Set[Dependency]:
        """
        Apply strategies to reduce false positives
        
        Strategies:
        1. Remove dependencies with very low confidence
        2. Deduplicate by name+version+ecosystem
        3. Filter out common false positives (if needed)
        """
        # Dependencies are already in a set, which handles basic deduplication
        # Additional filtering can be added here
        
        filtered = set()
        seen = {}
        
        for dep in dependencies:
            key = (dep.name.lower(), dep.ecosystem)
            
            # If we've seen this package before, keep the one with higher confidence
            if key in seen:
                existing = seen[key]
                # If versions match, keep higher confidence
                if dep.version == existing.version:
                    if dep.confidence > existing.confidence:
                        filtered.remove(existing)
                        filtered.add(dep)
                        seen[key] = dep
                else:
                    # Different versions, keep both
                    filtered.add(dep)
            else:
                filtered.add(dep)
                seen[key] = dep
        
        return filtered

