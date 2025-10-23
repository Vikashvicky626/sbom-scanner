"""
Mbed OS (ARM Embedded) dependency detector
"""
import json
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class MbedDetector(BaseDetector):
    """Detector for Mbed OS ARM embedded projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['mbed_lib.json', 'mbed.lib', 'mbed_app.json']
    
    def detect(self, path: Path) -> bool:
        """Check if Mbed manifest files exist"""
        return len(self.find_files(path, self.get_manifest_files())) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Mbed dependencies"""
        dependencies = set()
        
        # Parse mbed_lib.json files
        mbed_lib_json = self.find_files(path, ['mbed_lib.json'])
        for lib_file in mbed_lib_json:
            dependencies.update(self._parse_mbed_lib_json(lib_file, path))
        
        # Parse mbed_app.json files
        mbed_app_json = self.find_files(path, ['mbed_app.json'])
        for app_file in mbed_app_json:
            dependencies.update(self._parse_mbed_app_json(app_file, path))
        
        # Parse .lib files (references to other libraries)
        mbed_lib_files = self.find_files(path, ['*.lib'])
        for lib_file in mbed_lib_files:
            dependencies.update(self._parse_mbed_lib_file(lib_file, path))
        
        return dependencies
    
    def _parse_mbed_lib_json(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse mbed_lib.json file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse dependencies if present
            if 'dependencies' in data:
                for dep_name in data['dependencies']:
                    dep = Dependency(
                        name=dep_name,
                        version="*",
                        ecosystem=Ecosystem.MBED,
                        purl=f"pkg:mbed/{dep_name}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=0.95
                    )
                    dependencies.add(dep)
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_mbed_app_json(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse mbed_app.json file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse requires if present
            if 'requires' in data:
                requires = data['requires']
                if isinstance(requires, list):
                    for dep_name in requires:
                        dep = Dependency(
                            name=dep_name,
                            version="*",
                            ecosystem=Ecosystem.MBED,
                            purl=f"pkg:mbed/{dep_name}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=0.95
                        )
                        dependencies.add(dep)
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_mbed_lib_file(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """
        Parse .lib file (contains URL to library repository)
        Format: https://github.com/user/library-name/#revision
        """
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                url = f.read().strip()
            
            # Extract library name from URL
            # Pattern: https://github.com/user/library-name or similar
            if url:
                # Get library name from file name (more reliable)
                lib_name = file_path.stem  # filename without .lib extension
                
                # Try to extract version/revision from URL
                version = "*"
                if '#' in url:
                    version = url.split('#')[-1]
                
                dep = Dependency(
                    name=lib_name,
                    version=version,
                    ecosystem=Ecosystem.MBED,
                    purl=f"pkg:mbed/{lib_name}@{version}" if version != "*" else f"pkg:mbed/{lib_name}",
                    dependency_type=DependencyType.DIRECT,
                    source_file=str(file_path.relative_to(base_path)),
                    confidence=0.9
                )
                dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies

