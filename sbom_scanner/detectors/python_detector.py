"""
Python dependency detector
"""
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class PythonDetector(BaseDetector):
    """Detector for Python projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['requirements.txt', 'setup.py', 'Pipfile', 'pyproject.toml', 'setup.cfg']
    
    def detect(self, path: Path) -> bool:
        """Check if Python dependency files exist"""
        return len(self.find_files(path, self.get_manifest_files())) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Python dependencies"""
        dependencies = set()
        
        # Parse requirements.txt files
        req_files = self.find_files(path, ['requirements.txt'])
        for req_file in req_files:
            dependencies.update(self._parse_requirements_txt(req_file, path))
        
        # Parse setup.py files
        setup_files = self.find_files(path, ['setup.py'])
        for setup_file in setup_files:
            dependencies.update(self._parse_setup_py(setup_file, path))
        
        # Parse Pipfile
        pipfiles = self.find_files(path, ['Pipfile'])
        for pipfile in pipfiles:
            dependencies.update(self._parse_pipfile(pipfile, path))
        
        # Parse pyproject.toml
        pyproject_files = self.find_files(path, ['pyproject.toml'])
        for pyproject_file in pyproject_files:
            dependencies.update(self._parse_pyproject_toml(pyproject_file, path))
        
        return dependencies
    
    def _parse_requirements_txt(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse requirements.txt file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#') or line.startswith('-'):
                        continue
                    
                    # Parse package name and version
                    match = re.match(r'^([a-zA-Z0-9_\-\.\[\]]+)\s*([=<>!]+)\s*([0-9a-zA-Z\.\-\+]+)', line)
                    if match:
                        name = match.group(1)
                        version = match.group(3)
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.PYPI,
                            purl=f"pkg:pypi/{name}@{version}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
                    else:
                        # Handle package without version specifier
                        name_match = re.match(r'^([a-zA-Z0-9_\-\.\[\]]+)', line)
                        if name_match:
                            name = name_match.group(1)
                            dep = Dependency(
                                name=name,
                                version="*",
                                ecosystem=Ecosystem.PYPI,
                                purl=f"pkg:pypi/{name}",
                                dependency_type=DependencyType.DIRECT,
                                source_file=str(file_path.relative_to(base_path)),
                                confidence=0.9
                            )
                            dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_setup_py(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse setup.py file (basic parsing)"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for install_requires
            match = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if match:
                requires = match.group(1)
                # Extract quoted strings
                packages = re.findall(r'["\']([^"\']+)["\']', requires)
                
                for pkg in packages:
                    pkg = pkg.strip()
                    # Parse package name and version
                    match = re.match(r'^([a-zA-Z0-9_\-\.\[\]]+)\s*([=<>!]+)\s*([0-9a-zA-Z\.\-\+]+)', pkg)
                    if match:
                        name = match.group(1)
                        version = match.group(3)
                    else:
                        name_match = re.match(r'^([a-zA-Z0-9_\-\.\[\]]+)', pkg)
                        if name_match:
                            name = name_match.group(1)
                            version = "*"
                        else:
                            continue
                    
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.PYPI,
                        purl=f"pkg:pypi/{name}@{version}" if version != "*" else f"pkg:pypi/{name}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=0.95
                    )
                    dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_pipfile(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse Pipfile"""
        dependencies = set()
        
        try:
            import toml
            with open(file_path, 'r', encoding='utf-8') as f:
                data = toml.load(f)
            
            # Parse packages
            if 'packages' in data:
                for name, version_spec in data['packages'].items():
                    if isinstance(version_spec, dict):
                        version = version_spec.get('version', '*').strip()
                    else:
                        version = str(version_spec).strip()
                    
                    # Clean version
                    version = version.strip('"\'')
                    if version.startswith('=='):
                        version = version[2:].strip()
                    
                    dep = Dependency(
                        name=name,
                        version=version if version != '*' else '*',
                        ecosystem=Ecosystem.PYPI,
                        purl=f"pkg:pypi/{name}@{version}" if version != '*' else f"pkg:pypi/{name}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=1.0
                    )
                    dependencies.add(dep)
            
            # Parse dev-packages
            if 'dev-packages' in data:
                for name, version_spec in data['dev-packages'].items():
                    if isinstance(version_spec, dict):
                        version = version_spec.get('version', '*').strip()
                    else:
                        version = str(version_spec).strip()
                    
                    version = version.strip('"\'')
                    if version.startswith('=='):
                        version = version[2:].strip()
                    
                    dep = Dependency(
                        name=name,
                        version=version if version != '*' else '*',
                        ecosystem=Ecosystem.PYPI,
                        purl=f"pkg:pypi/{name}@{version}" if version != '*' else f"pkg:pypi/{name}",
                        dependency_type=DependencyType.DEV,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=1.0
                    )
                    dependencies.add(dep)
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_pyproject_toml(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse pyproject.toml file"""
        dependencies = set()
        
        try:
            import toml
            with open(file_path, 'r', encoding='utf-8') as f:
                data = toml.load(f)
            
            # Poetry dependencies
            if 'tool' in data and 'poetry' in data['tool']:
                poetry = data['tool']['poetry']
                
                if 'dependencies' in poetry:
                    for name, version_spec in poetry['dependencies'].items():
                        if name == 'python':  # Skip python version itself
                            continue
                        
                        if isinstance(version_spec, dict):
                            version = version_spec.get('version', '*')
                        else:
                            version = str(version_spec)
                        
                        version = version.strip('"\'')
                        if version.startswith('^') or version.startswith('~'):
                            version = version[1:].strip()
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.PYPI,
                            purl=f"pkg:pypi/{name}@{version}" if version != '*' else f"pkg:pypi/{name}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
            
            # PEP 621 dependencies
            if 'project' in data and 'dependencies' in data['project']:
                for dep_string in data['project']['dependencies']:
                    match = re.match(r'^([a-zA-Z0-9_\-\.\[\]]+)\s*([=<>!]+)\s*([0-9a-zA-Z\.\-\+]+)', dep_string)
                    if match:
                        name = match.group(1)
                        version = match.group(3)
                    else:
                        name_match = re.match(r'^([a-zA-Z0-9_\-\.\[\]]+)', dep_string)
                        if name_match:
                            name = name_match.group(1)
                            version = "*"
                        else:
                            continue
                    
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.PYPI,
                        purl=f"pkg:pypi/{name}@{version}" if version != '*' else f"pkg:pypi/{name}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(file_path.relative_to(base_path)),
                        confidence=1.0
                    )
                    dependencies.add(dep)
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies

