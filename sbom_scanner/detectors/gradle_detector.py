"""
Gradle dependency detector
"""
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class GradleDetector(BaseDetector):
    """Detector for Gradle projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['build.gradle', 'build.gradle.kts']
    
    def detect(self, path: Path) -> bool:
        """Check if build.gradle or build.gradle.kts exists"""
        return len(self.find_files(path, self.get_manifest_files())) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Gradle dependencies"""
        dependencies = set()
        
        gradle_files = self.find_files(path, self.get_manifest_files())
        
        for gradle_file in gradle_files:
            try:
                with open(gradle_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Pattern for dependencies like: implementation 'group:artifact:version'
                pattern1 = r'(?:implementation|api|compile|testImplementation|testCompile|runtimeOnly|compileOnly)\s+["\']([^:]+):([^:]+):([^"\']+)["\']'
                matches = re.findall(pattern1, content)
                
                for match in matches:
                    group_id, artifact_id, version = match
                    name = f"{group_id}:{artifact_id}"
                    
                    # Determine dependency type based on configuration
                    dep_type = DependencyType.DIRECT
                    if 'test' in content.lower():
                        dep_type = DependencyType.DEV
                    
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.GRADLE,
                        purl=f"pkg:maven/{group_id}/{artifact_id}@{version}",
                        dependency_type=dep_type,
                        source_file=str(gradle_file.relative_to(path)),
                        confidence=0.95
                    )
                    dependencies.add(dep)
                
                # Pattern for dependencies with group, name, version separately
                pattern2 = r'(?:implementation|api|compile|testImplementation|testCompile|runtimeOnly|compileOnly)\s+group\s*:\s*["\']([^"\']+)["\']\s*,\s*name\s*:\s*["\']([^"\']+)["\']\s*,\s*version\s*:\s*["\']([^"\']+)["\']'
                matches2 = re.findall(pattern2, content)
                
                for match in matches2:
                    group_id, artifact_id, version = match
                    name = f"{group_id}:{artifact_id}"
                    
                    dep = Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.GRADLE,
                        purl=f"pkg:maven/{group_id}/{artifact_id}@{version}",
                        dependency_type=DependencyType.DIRECT,
                        source_file=str(gradle_file.relative_to(path)),
                        confidence=0.95
                    )
                    dependencies.add(dep)
            
            except IOError as e:
                print(f"Warning: Could not parse {gradle_file}: {e}")
                continue
        
        return dependencies

