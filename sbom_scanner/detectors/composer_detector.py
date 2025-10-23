"""
Composer (PHP) dependency detector
"""
import json
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class ComposerDetector(BaseDetector):
    """Detector for Composer/PHP projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['composer.json', 'composer.lock']
    
    def detect(self, path: Path) -> bool:
        """Check if composer.json exists"""
        return len(self.find_files(path, ['composer.json'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Composer dependencies from composer.json"""
        dependencies = set()
        
        composer_files = self.find_files(path, ['composer.json'])
        
        for composer_file in composer_files:
            try:
                with open(composer_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Parse regular dependencies
                if 'require' in data:
                    for name, version in data['require'].items():
                        # Skip PHP itself
                        if name == 'php' or name.startswith('ext-'):
                            continue
                        
                        dep = Dependency(
                            name=name,
                            version=self._clean_version(version),
                            ecosystem=Ecosystem.COMPOSER,
                            purl=f"pkg:composer/{name}@{self._clean_version(version)}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(composer_file.relative_to(path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
                
                # Parse dev dependencies
                if 'require-dev' in data:
                    for name, version in data['require-dev'].items():
                        if name == 'php' or name.startswith('ext-'):
                            continue
                        
                        dep = Dependency(
                            name=name,
                            version=self._clean_version(version),
                            ecosystem=Ecosystem.COMPOSER,
                            purl=f"pkg:composer/{name}@{self._clean_version(version)}",
                            dependency_type=DependencyType.DEV,
                            source_file=str(composer_file.relative_to(path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not parse {composer_file}: {e}")
                continue
        
        return dependencies
    
    def _clean_version(self, version: str) -> str:
        """Remove version prefixes like ^, ~, >=, etc."""
        version = version.strip()
        for prefix in ['^', '~', '>=', '<=', '>', '<', '=']:
            if version.startswith(prefix):
                version = version[len(prefix):].strip()
        return version if version else "*"

