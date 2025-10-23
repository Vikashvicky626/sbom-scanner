# SBOM Scanner - Quick Start Guide

Get started with SBOM Scanner in 5 minutes!

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/sbom-scanner.git
cd sbom-scanner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install the tool
pip install -e .
```

## Verify Installation

```bash
sbom-scan --version
```

You should see: `SBOM Scanner v1.0.0`

## Your First Scan

### Test with Example Project

We've included a multi-language example project:

```bash
sbom-scan examples/multi_language_project -o example-sbom.json
```

This will scan the example project which contains:
- JavaScript (package.json)
- Python (requirements.txt)
- Java (pom.xml)
- Go (go.mod)

Output: `example-sbom.json`

### Scan Your Own Project

```bash
# Navigate to your project
cd /path/to/your/project

# Run the scanner
sbom-scan
```

That's it! You'll find `sbom.json` in your project directory.

## What Just Happened?

The scanner:
1. ✅ Detected all package managers in your project
2. ✅ Extracted dependencies with versions
3. ✅ Generated a CycloneDX format SBOM
4. ✅ Filtered out false positives (confidence threshold: 0.8)

## View Your SBOM

```bash
# Pretty print JSON
cat sbom.json | python -m json.tool

# Count dependencies
cat sbom.json | grep -c '"name"'

# Extract component names
cat sbom.json | jq '.components[].name'
```

## Common Use Cases

### 1. Security Scanning

Feed your SBOM to a vulnerability scanner:

```bash
# Generate SBOM
sbom-scan -o sbom.json

# Use with Grype (example)
grype sbom:sbom.json
```

### 2. License Compliance

```bash
# Generate SBOM for compliance team
sbom-scan -n "ProductName" -v "1.0.0" -o sbom-v1.0.0.json
```

### 3. CI/CD Pipeline

Add to your build script:

```bash
#!/bin/bash
echo "Building application..."
# ... your build steps ...

echo "Generating SBOM..."
sbom-scan -o build/sbom.json -n "MyApp" -v "$BUILD_VERSION"
```

### 4. XML Format (for tools that require it)

```bash
sbom-scan -f xml -o sbom.xml
```

## Customize Your Scan

### Reduce False Positives

```bash
# Strict mode (higher confidence threshold)
sbom-scan --min-confidence 0.9
```

### Include More Dependencies

```bash
# Permissive mode (lower confidence threshold)
sbom-scan --min-confidence 0.7
```

### Specify Project Metadata

```bash
sbom-scan \
  --project-name "MyApplication" \
  --project-version "2.1.0" \
  -o sbom-v2.1.0.json
```

## Next Steps

1. **Read the full documentation**: See `README.md`
2. **Explore usage examples**: Check `USAGE.md`
3. **Integrate with CI/CD**: See integration examples in `USAGE.md`
4. **Contribute**: See `CONTRIBUTING.md` to add support for more languages

## Troubleshooting

### No dependencies found?

```bash
# Check what files exist
ls -la

# Run with verbose output
sbom-scan --verbose
```

### Python module errors?

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Need help?

- Check `USAGE.md` for detailed documentation
- Open an issue on GitHub
- Email: support@example.com

## Example Output

Here's what a generated SBOM looks like:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "metadata": {
    "component": {
      "type": "application",
      "name": "my-project",
      "version": "1.0.0"
    },
    "tools": [
      {
        "name": "sbom-scanner",
        "version": "1.0.0"
      }
    ]
  },
  "components": [
    {
      "type": "library",
      "name": "express",
      "version": "4.18.2",
      "purl": "pkg:npm/express@4.18.2"
    },
    {
      "type": "library",
      "name": "requests",
      "version": "2.31.0",
      "purl": "pkg:pypi/requests@2.31.0"
    }
  ]
}
```

## Supported Languages

✅ JavaScript/TypeScript (npm, yarn, pnpm)  
✅ Python (pip, poetry, pipenv)  
✅ Java (Maven, Gradle)  
✅ PHP (Composer)  
✅ .NET (NuGet)  
✅ Ruby (Gem)  
✅ Rust (Cargo)  
✅ Go (go modules)

## Pro Tips

1. **Commit SBOMs to version control** to track dependency changes over time
2. **Generate SBOMs on every release** for security auditing
3. **Use strict mode (0.9+)** for production deployments
4. **Scan regularly** to catch new vulnerabilities
5. **Integrate with security tools** like Dependency-Track

---

**You're all set! Happy scanning! 🚀**

For detailed documentation, see `README.md` and `USAGE.md`.

