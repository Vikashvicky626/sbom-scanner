"""
Maven dependency detector
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class MavenDetector(BaseDetector):
    """Detector for Maven projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['pom.xml']
    
    def detect(self, path: Path) -> bool:
        """Check if pom.xml exists"""
        return len(self.find_files(path, ['pom.xml'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Maven dependencies from pom.xml"""
        dependencies = set()
        
        pom_files = self.find_files(path, ['pom.xml'])
        
        for pom_file in pom_files:
            try:
                tree = ET.parse(pom_file)
                root = tree.getroot()
                
                # Handle XML namespace
                namespace = {'maven': 'http://maven.apache.org/POM/4.0.0'}
                if root.tag.startswith('{'):
                    ns = root.tag.split('}')[0] + '}'
                    namespace = {'maven': ns.strip('{}')}
                
                # Parse dependencies
                deps_element = root.find('.//maven:dependencies', namespace)
                if deps_element is None:
                    # Try without namespace
                    deps_element = root.find('.//dependencies')
                
                if deps_element is not None:
                    for dep in deps_element.findall('.//maven:dependency', namespace):
                        if dep is None:
                            dep = deps_element.findall('.//dependency')
                            if not dep:
                                continue
                            dep = dep[0]
                        
                        group_id = self._get_element_text(dep, 'groupId', namespace)
                        artifact_id = self._get_element_text(dep, 'artifactId', namespace)
                        version = self._get_element_text(dep, 'version', namespace)
                        scope = self._get_element_text(dep, 'scope', namespace)
                        
                        if group_id and artifact_id:
                            name = f"{group_id}:{artifact_id}"
                            version = version if version else "*"
                            
                            dep_type = DependencyType.DEV if scope == 'test' else DependencyType.DIRECT
                            
                            dependency = Dependency(
                                name=name,
                                version=version,
                                ecosystem=Ecosystem.MAVEN,
                                purl=f"pkg:maven/{group_id}/{artifact_id}@{version}" if version != "*" else f"pkg:maven/{group_id}/{artifact_id}",
                                dependency_type=dep_type,
                                source_file=str(pom_file.relative_to(path)),
                                confidence=1.0
                            )
                            dependencies.add(dependency)
            
            except (ET.ParseError, IOError) as e:
                print(f"Warning: Could not parse {pom_file}: {e}")
                continue
        
        return dependencies
    
    def _get_element_text(self, parent, tag_name, namespace):
        """Get text from XML element, trying with and without namespace"""
        element = parent.find(f"maven:{tag_name}", namespace)
        if element is None:
            element = parent.find(tag_name)
        return element.text if element is not None else None

