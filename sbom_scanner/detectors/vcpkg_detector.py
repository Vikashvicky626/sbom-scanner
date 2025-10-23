"""
vcpkg (C/C++) dependency detector
"""
import json
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class VcpkgDetector(BaseDetector):
    """Detector for vcpkg C/C++ projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['vcpkg.json', 'vcpkg-configuration.json']
    
    def detect(self, path: Path) -> bool:
        """Check if vcpkg manifest files exist"""
        return len(self.find_files(path, ['vcpkg.json'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse vcpkg dependencies from vcpkg.json"""
        dependencies = set()
        
        vcpkg_files = self.find_files(path, ['vcpkg.json'])
        
        for vcpkg_file in vcpkg_files:
            try:
                with open(vcpkg_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Parse dependencies array
                if 'dependencies' in data:
                    for dep_entry in data['dependencies']:
                        # Can be string or object
                        if isinstance(dep_entry, str):
                            name = dep_entry
                            version = "*"
                            confidence = 0.9
                        elif isinstance(dep_entry, dict):
                            name = dep_entry.get('name', '')
                            version = dep_entry.get('version', '*')
                            
                            # Handle version constraints
                            if 'version>=' in dep_entry:
                                version = dep_entry['version>=']
                            elif 'version-string' in dep_entry:
                                version = dep_entry['version-string']
                            
                            confidence = 1.0
                        else:
                            continue
                        
                        if name:
                            dep = Dependency(
                                name=name,
                                version=version,
                                ecosystem=Ecosystem.VCPKG,
                                purl=f"pkg:vcpkg/{name}@{version}" if version != "*" else f"pkg:vcpkg/{name}",
                                dependency_type=DependencyType.DIRECT,
                                source_file=str(vcpkg_file.relative_to(path)),
                                confidence=confidence
                            )
                            dependencies.add(dep)
                
                # Parse dev-dependencies
                if 'dev-dependencies' in data:
                    for dep_entry in data['dev-dependencies']:
                        if isinstance(dep_entry, str):
                            name = dep_entry
                            version = "*"
                        elif isinstance(dep_entry, dict):
                            name = dep_entry.get('name', '')
                            version = dep_entry.get('version', '*')
                        else:
                            continue
                        
                        if name:
                            dep = Dependency(
                                name=name,
                                version=version,
                                ecosystem=Ecosystem.VCPKG,
                                purl=f"pkg:vcpkg/{name}@{version}" if version != "*" else f"pkg:vcpkg/{name}",
                                dependency_type=DependencyType.DEV,
                                source_file=str(vcpkg_file.relative_to(path)),
                                confidence=0.95
                            )
                            dependencies.add(dep)
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not parse {vcpkg_file}: {e}")
                continue
        
        return dependencies

