"""
Base detector class for all language-specific detectors
"""
from abc import ABC, abstractmethod
from typing import List, Set
from pathlib import Path
from ..models import Dependency


class BaseDetector(ABC):
    """Base class for all package manager detectors"""
    
    @abstractmethod
    def detect(self, path: Path) -> bool:
        """
        Check if this detector should be used for the given path
        Returns True if relevant manifest files are found
        """
        pass
    
    @abstractmethod
    def parse(self, path: Path) -> Set[Dependency]:
        """
        Parse dependencies from the project at the given path
        Returns a set of Dependency objects
        """
        pass
    
    @abstractmethod
    def get_manifest_files(self) -> List[str]:
        """
        Return list of manifest file names this detector looks for
        """
        pass
    
    def find_files(self, path: Path, filenames: List[str]) -> List[Path]:
        """
        Recursively find all files matching the given filenames
        """
        found_files = []
        for filename in filenames:
            # Search recursively
            for file_path in path.rglob(filename):
                # Skip node_modules, vendor, and other common dependency directories
                if self._should_skip_path(file_path):
                    continue
                found_files.append(file_path)
        return found_files
    
    def _should_skip_path(self, file_path: Path) -> bool:
        """
        Check if path should be skipped (e.g., in vendor/node_modules directories)
        This helps reduce false positives from nested dependencies
        """
        skip_dirs = {
            'node_modules',
            'vendor',
            'bower_components',
            '.git',
            '__pycache__',
            'venv',
            'env',
            '.venv',
            'virtualenv',
            'target',
            'build',
            'dist',
            '.gradle',
            'gradle',
            'obj',
            'bin',
        }
        
        # Check if any parent directory should be skipped
        for parent in file_path.parents:
            if parent.name in skip_dirs:
                return True
        
        return False

