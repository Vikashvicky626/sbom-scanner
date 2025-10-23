"""
Conan (C/C++) dependency detector
"""
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class ConanDetector(BaseDetector):
    """Detector for Conan C/C++ projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['conanfile.txt', 'conanfile.py', 'conan.lock']
    
    def detect(self, path: Path) -> bool:
        """Check if Conan manifest files exist"""
        return len(self.find_files(path, self.get_manifest_files())) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Conan dependencies"""
        dependencies = set()
        
        # Parse conanfile.txt files
        conanfile_txt = self.find_files(path, ['conanfile.txt'])
        for conan_file in conanfile_txt:
            dependencies.update(self._parse_conanfile_txt(conan_file, path))
        
        # Parse conanfile.py files
        conanfile_py = self.find_files(path, ['conanfile.py'])
        for conan_file in conanfile_py:
            dependencies.update(self._parse_conanfile_py(conan_file, path))
        
        # Parse conan.lock files
        conan_lock = self.find_files(path, ['conan.lock'])
        for lock_file in conan_lock:
            dependencies.update(self._parse_conan_lock(lock_file, path))
        
        return dependencies
    
    def _parse_conanfile_txt(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse conanfile.txt file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find [requires] section
            requires_match = re.search(r'\[requires\](.*?)(?:\[|$)', content, re.DOTALL)
            if requires_match:
                requires_section = requires_match.group(1)
                
                # Parse lines like: package/version@user/channel
                # or: package/version
                for line in requires_section.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Pattern: package/version@user/channel or package/version
                    match = re.match(r'^([a-zA-Z0-9_\-\.]+)/([0-9a-zA-Z\.\-\+]+)', line)
                    if match:
                        name = match.group(1)
                        version = match.group(2)
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.CONAN,
                            purl=f"pkg:conan/{name}@{version}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_conanfile_py(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse conanfile.py file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for requires = () or self.requires()
            # Pattern 1: requires = ("package/version", ...)
            requires_tuple = re.findall(r'requires\s*=\s*\((.*?)\)', content, re.DOTALL)
            for requires in requires_tuple:
                # Extract quoted strings
                packages = re.findall(r'["\']([^"\']+/[^"\']+)["\']', requires)
                for pkg in packages:
                    match = re.match(r'^([a-zA-Z0-9_\-\.]+)/([0-9a-zA-Z\.\-\+]+)', pkg)
                    if match:
                        name = match.group(1)
                        version = match.group(2)
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.CONAN,
                            purl=f"pkg:conan/{name}@{version}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=0.95
                        )
                        dependencies.add(dep)
            
            # Pattern 2: self.requires("package/version")
            self_requires = re.findall(r'self\.requires\(["\']([^"\']+/[^"\']+)["\']\)', content)
            for pkg in self_requires:
                match = re.match(r'^([a-zA-Z0-9_\-\.]+)/([0-9a-zA-Z\.\-\+]+)', pkg)
                if match:
                    name = match.group(1)
                    version = match.group(2)
                    
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.CONAN,
                        purl=f"pkg:conan/{name}@{version}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=0.95
                    )
                    dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_conan_lock(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse conan.lock file (JSON format)"""
        dependencies = set()
        
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse graph_lock.nodes
            if 'graph_lock' in data and 'nodes' in data['graph_lock']:
                for node_id, node_data in data['graph_lock']['nodes'].items():
                    if node_id == '0':  # Skip root node
                        continue
                    
                    ref = node_data.get('ref', '')
                    if ref:
                        # Parse ref like: package/version@user/channel
                        match = re.match(r'^([a-zA-Z0-9_\-\.]+)/([0-9a-zA-Z\.\-\+]+)', ref)
                        if match:
                            name = match.group(1)
                            version = match.group(2)
                            
                            dep = Dependency(
                                name=name,
                                version=version,
                                ecosystem=Ecosystem.CONAN,
                                purl=f"pkg:conan/{name}@{version}",
                                dependency_type=DependencyType.DIRECT,
                                source_file=str(file_path.relative_to(base_path)),
                                confidence=1.0  # Lock file has highest confidence
                            )
                            dependencies.add(dep)
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies

