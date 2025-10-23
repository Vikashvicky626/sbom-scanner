"""
Rust (Cargo) dependency detector
"""
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class RustDetector(BaseDetector):
    """Detector for Rust/Cargo projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['Cargo.toml', 'Cargo.lock']
    
    def detect(self, path: Path) -> bool:
        """Check if Cargo.toml exists"""
        return len(self.find_files(path, ['Cargo.toml'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Rust dependencies from Cargo.toml"""
        dependencies = set()
        
        cargo_files = self.find_files(path, ['Cargo.toml'])
        
        for cargo_file in cargo_files:
            try:
                import toml
                with open(cargo_file, 'r', encoding='utf-8') as f:
                    data = toml.load(f)
                
                # Parse dependencies
                if 'dependencies' in data:
                    for name, version_spec in data['dependencies'].items():
                        if isinstance(version_spec, dict):
                            version = version_spec.get('version', '*')
                        else:
                            version = str(version_spec)
                        
                        version = version.strip('"\'')
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.CARGO,
                            purl=f"pkg:cargo/{name}@{version}" if version != '*' else f"pkg:cargo/{name}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(cargo_file.relative_to(path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
                
                # Parse dev dependencies
                if 'dev-dependencies' in data:
                    for name, version_spec in data['dev-dependencies'].items():
                        if isinstance(version_spec, dict):
                            version = version_spec.get('version', '*')
                        else:
                            version = str(version_spec)
                        
                        version = version.strip('"\'')
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.CARGO,
                            purl=f"pkg:cargo/{name}@{version}" if version != '*' else f"pkg:cargo/{name}",
                            dependency_type=DependencyType.DEV,
                            source_file=str(cargo_file.relative_to(path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
            
            except Exception as e:
                print(f"Warning: Could not parse {cargo_file}: {e}")
                continue
        
        return dependencies

