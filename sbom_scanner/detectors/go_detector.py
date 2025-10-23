"""
Go dependency detector
"""
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class GoDetector(BaseDetector):
    """Detector for Go projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['go.mod', 'go.sum']
    
    def detect(self, path: Path) -> bool:
        """Check if go.mod exists"""
        return len(self.find_files(path, ['go.mod'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Go dependencies from go.mod"""
        dependencies = set()
        
        go_mod_files = self.find_files(path, ['go.mod'])
        
        for go_mod_file in go_mod_files:
            try:
                with open(go_mod_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse require statements
                # Pattern for single-line require
                pattern1 = r'require\s+([^\s]+)\s+v?([^\s]+)'
                matches = re.findall(pattern1, content)
                
                for name, version in matches:
                    if name == '(' or name == ')':
                        continue
                    
                    version = version.strip()
                    if version.endswith(')'):
                        version = version[:-1].strip()
                    
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.GO,
                        purl=f"pkg:golang/{name}@{version}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(go_mod_file.relative_to(path)),
                        confidence=1.0
                    )
                    dependencies.add(dep)
                
                # Parse multi-line require blocks
                require_blocks = re.findall(r'require\s*\((.*?)\)', content, re.DOTALL)
                for block in require_blocks:
                    lines = block.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('//'):
                            continue
                        
                        match = re.match(r'([^\s]+)\s+v?([^\s]+)', line)
                        if match:
                            name, version = match.groups()
                            
                            dep = Dependency(
                                name=name,
                                version=version,
                                ecosystem=Ecosystem.GO,
                                purl=f"pkg:golang/{name}@{version}",
                                dependency_type=DependencyType.DIRECT,
                                source_file=str(go_mod_file.relative_to(path)),
                                confidence=1.0
                            )
                            dependencies.add(dep)
            
            except IOError as e:
                print(f"Warning: Could not parse {go_mod_file}: {e}")
                continue
        
        return dependencies

