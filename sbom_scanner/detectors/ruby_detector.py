"""
Ruby (Gem) dependency detector
"""
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class RubyDetector(BaseDetector):
    """Detector for Ruby/Gem projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['Gemfile', 'Gemfile.lock', '*.gemspec']
    
    def detect(self, path: Path) -> bool:
        """Check if Gemfile exists"""
        return len(self.find_files(path, ['Gemfile'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Ruby dependencies from Gemfile"""
        dependencies = set()
        
        gemfiles = self.find_files(path, ['Gemfile'])
        
        for gemfile in gemfiles:
            try:
                with open(gemfile, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Pattern for gem 'name', 'version' or gem "name", "version"
                pattern1 = r'gem\s+["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
                matches = re.findall(pattern1, content)
                
                for name, version in matches:
                    version = self._clean_version(version)
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.GEM,
                        purl=f"pkg:gem/{name}@{version}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(gemfile.relative_to(path)),
                        confidence=1.0
                    )
                    dependencies.add(dep)
                
                # Pattern for gem 'name' without version
                pattern2 = r'gem\s+["\']([^"\']+)["\'](?!\s*,)'
                matches2 = re.findall(pattern2, content)
                
                for name in matches2:
                    dep = Dependency(
                        name=name,
                        version="*",
                        ecosystem=Ecosystem.GEM,
                        purl=f"pkg:gem/{name}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(gemfile.relative_to(path)),
                        confidence=0.9
                    )
                    dependencies.add(dep)
            
            except IOError as e:
                print(f"Warning: Could not parse {gemfile}: {e}")
                continue
        
        return dependencies
    
    def _clean_version(self, version: str) -> str:
        """Remove version operators"""
        version = version.strip()
        for prefix in ['~>', '>=', '<=', '>', '<', '=']:
            if version.startswith(prefix):
                version = version[len(prefix):].strip()
        return version if version else "*"

