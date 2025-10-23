"""
CycloneDX BOM generator
"""
import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
try:
    from cyclonedx.model import Tool
except ImportError:
    from cyclonedx.model.tool import Tool
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output.json import JsonV1Dot5
from cyclonedx.output.xml import XmlV1Dot5
from packageurl import PackageURL

from .models import ScanResult, Ecosystem, DependencyType


class CycloneDXGenerator:
    """Generate CycloneDX SBOM from scan results"""
    
    def __init__(self):
        self.tool_name = "sbom-scanner"
        self.tool_version = "1.0.0"
    
    def generate(self, scan_result: ScanResult, output_format: str = "json") -> str:
        """
        Generate CycloneDX BOM
        
        Args:
            scan_result: ScanResult from scanner
            output_format: "json" or "xml"
        
        Returns:
            Serialized BOM as string
        """
        # Create BOM
        bom = Bom()
        
        # Add metadata
        try:
            tool = Tool(name=self.tool_name, version=self.tool_version)
            bom.metadata.tools.add(tool)
        except Exception:
            # Fallback for different cyclonedx-python-lib versions
            pass
        
        # Create main component (the project being scanned)
        try:
            main_component = Component(
                name=scan_result.project_name,
                version=scan_result.project_version,
                type=ComponentType.APPLICATION
            )
            bom.metadata.component = main_component
        except TypeError:
            # Older version of cyclonedx-python-lib
            main_component = Component(
                name=scan_result.project_name,
                version=scan_result.project_version
            )
            main_component.type = ComponentType.APPLICATION
            bom.metadata.component = main_component
        
        # Add dependencies as components
        for dep in scan_result.dependencies:
            component = self._create_component(dep)
            if component:
                bom.components.add(component)
        
        # Serialize BOM
        if output_format.lower() == "json":
            outputter = JsonV1Dot5(bom)
            return outputter.output_as_string()
        elif output_format.lower() == "xml":
            outputter = XmlV1Dot5(bom)
            return outputter.output_as_string()
        else:
            raise ValueError(f"Unsupported format: {output_format}. Use 'json' or 'xml'")
    
    def _create_component(self, dep) -> Component:
        """Create a CycloneDX Component from a Dependency"""
        try:
            # Determine component type based on dependency type
            comp_type = ComponentType.LIBRARY
            
            # Create PackageURL
            if dep.purl:
                purl = PackageURL.from_string(dep.purl)
            else:
                # Construct PURL if not provided
                purl = self._construct_purl(dep)
            
            # Create component
            try:
                component = Component(
                    name=dep.name,
                    version=dep.version if dep.version != "*" else None,
                    type=comp_type,
                    purl=purl
                )
            except TypeError:
                # Older API
                component = Component(
                    name=dep.name,
                    version=dep.version if dep.version != "*" else None
                )
                component.type = comp_type
                component.purl = purl
            
            # Add optional fields if available
            if dep.description:
                component.description = dep.description
            
            if dep.license:
                # Note: License handling in cyclonedx-python-lib is complex
                # You may need to use LicenseChoice and License objects
                pass
            
            return component
        
        except Exception as e:
            print(f"Warning: Could not create component for {dep.name}: {e}")
            return None
    
    def _construct_purl(self, dep) -> PackageURL:
        """Construct a PackageURL from dependency information"""
        ecosystem_map = {
            Ecosystem.NPM: "npm",
            Ecosystem.PYPI: "pypi",
            Ecosystem.MAVEN: "maven",
            Ecosystem.GRADLE: "maven",  # Gradle uses Maven repos
            Ecosystem.COMPOSER: "composer",
            Ecosystem.NUGET: "nuget",
            Ecosystem.GEM: "gem",
            Ecosystem.CARGO: "cargo",
            Ecosystem.GO: "golang",
            Ecosystem.CONAN: "conan",
            Ecosystem.VCPKG: "vcpkg",
            Ecosystem.CMAKE: "generic",  # CMake deps are generic
            Ecosystem.PLATFORMIO: "platformio",
            Ecosystem.ARDUINO: "arduino",
            Ecosystem.MBED: "generic",  # Mbed uses generic type
        }
        
        purl_type = ecosystem_map.get(dep.ecosystem, "generic")
        
        # Handle Maven-style coordinates (group:artifact)
        if purl_type == "maven" and ":" in dep.name:
            parts = dep.name.split(":")
            namespace = parts[0]
            name = parts[1] if len(parts) > 1 else parts[0]
            
            return PackageURL(
                type=purl_type,
                namespace=namespace,
                name=name,
                version=dep.version if dep.version != "*" else None
            )
        else:
            return PackageURL(
                type=purl_type,
                name=dep.name,
                version=dep.version if dep.version != "*" else None
            )
    
    def save_to_file(self, scan_result: ScanResult, output_path: str, 
                     output_format: str = "json"):
        """
        Generate BOM and save to file
        
        Args:
            scan_result: ScanResult from scanner
            output_path: Path to save the BOM file
            output_format: "json" or "xml"
        """
        bom_content = self.generate(scan_result, output_format)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(bom_content)
        
        print(f"SBOM saved to: {output_file}")

