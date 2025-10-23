"""
NuGet (.NET) dependency detector
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class NuGetDetector(BaseDetector):
    """Detector for NuGet/.NET projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['packages.config', '*.csproj', '*.fsproj', '*.vbproj']
    
    def detect(self, path: Path) -> bool:
        """Check if .NET project files exist"""
        return (len(self.find_files(path, ['packages.config'])) > 0 or
                len(list(path.rglob('*.csproj'))) > 0 or
                len(list(path.rglob('*.fsproj'))) > 0)
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse NuGet dependencies"""
        dependencies = set()
        
        # Parse packages.config
        packages_files = self.find_files(path, ['packages.config'])
        for pkg_file in packages_files:
            dependencies.update(self._parse_packages_config(pkg_file, path))
        
        # Parse .csproj files
        csproj_files = [f for f in path.rglob('*.csproj') if not self._should_skip_path(f)]
        for csproj_file in csproj_files:
            dependencies.update(self._parse_project_file(csproj_file, path))
        
        # Parse .fsproj files
        fsproj_files = [f for f in path.rglob('*.fsproj') if not self._should_skip_path(f)]
        for fsproj_file in fsproj_files:
            dependencies.update(self._parse_project_file(fsproj_file, path))
        
        return dependencies
    
    def _parse_packages_config(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse packages.config file"""
        dependencies = set()
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for package in root.findall('.//package'):
                name = package.get('id')
                version = package.get('version')
                
                if name and version:
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.NUGET,
                        purl=f"pkg:nuget/{name}@{version}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=1.0
                    )
                    dependencies.add(dep)
        
        except (ET.ParseError, IOError) as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_project_file(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse .csproj/.fsproj file"""
        dependencies = set()
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find PackageReference elements
            for package_ref in root.findall('.//PackageReference'):
                name = package_ref.get('Include')
                version = package_ref.get('Version')
                
                if not version:
                    # Try to find Version as child element
                    version_elem = package_ref.find('Version')
                    if version_elem is not None:
                        version = version_elem.text
                
                if name:
                    version = version if version else "*"
                    
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.NUGET,
                        purl=f"pkg:nuget/{name}@{version}" if version != "*" else f"pkg:nuget/{name}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=1.0
                    )
                    dependencies.add(dep)
        
        except (ET.ParseError, IOError) as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies

