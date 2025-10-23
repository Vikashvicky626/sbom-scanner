"""
NPM/Node.js dependency detector
"""
import json
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class NpmDetector(BaseDetector):
    """Detector for NPM/Node.js projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml']
    
    def detect(self, path: Path) -> bool:
        """Check if package.json exists"""
        return len(self.find_files(path, ['package.json'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse NPM dependencies from package.json"""
        dependencies = set()
        
        package_json_files = self.find_files(path, ['package.json'])
        
        for package_file in package_json_files:
            try:
                with open(package_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Parse regular dependencies
                if 'dependencies' in data:
                    for name, version in data['dependencies'].items():
                        dep = Dependency(
                            name=name,
                            version=self._clean_version(version),
                            ecosystem=Ecosystem.NPM,
                            purl=f"pkg:npm/{name}@{self._clean_version(version)}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(package_file.relative_to(path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
                
                # Parse dev dependencies
                if 'devDependencies' in data:
                    for name, version in data['devDependencies'].items():
                        dep = Dependency(
                            name=name,
                            version=self._clean_version(version),
                            ecosystem=Ecosystem.NPM,
                            purl=f"pkg:npm/{name}@{self._clean_version(version)}",
                            dependency_type=DependencyType.DEV,
                            source_file=str(package_file.relative_to(path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
                
                # Parse peer dependencies
                if 'peerDependencies' in data:
                    for name, version in data['peerDependencies'].items():
                        dep = Dependency(
                            name=name,
                            version=self._clean_version(version),
                            ecosystem=Ecosystem.NPM,
                            purl=f"pkg:npm/{name}@{self._clean_version(version)}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(package_file.relative_to(path)),
                            confidence=0.9  # Slightly lower confidence for peer deps
                        )
                        dependencies.add(dep)
                
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not parse {package_file}: {e}")
                continue
        
        return dependencies
    
    def _clean_version(self, version: str) -> str:
        """Remove version prefixes like ^, ~, >=, etc."""
        version = version.strip()
        # Remove common npm version operators
        for prefix in ['^', '~', '>=', '<=', '>', '<', '=']:
            if version.startswith(prefix):
                version = version[len(prefix):].strip()
        return version if version else "latest"

