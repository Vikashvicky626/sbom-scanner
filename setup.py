from setuptools import setup, find_packages

setup(
    name="sbom-scanner",
    version="1.0.0",
    description="Multi-language SBOM scanner generating CycloneDX format output",
    author="SBOM Scanner Team",
    packages=find_packages(),
    install_requires=[
        "packageurl-python>=0.15.6",
        "cyclonedx-python-lib>=7.5.1",
        "pyyaml>=6.0.2",
        "toml>=0.10.2",
        "packaging>=24.1",
        "click>=8.1.7",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "sbom-scan=sbom_scanner.cli:main",
        ],
    },
    python_requires=">=3.8",
)

