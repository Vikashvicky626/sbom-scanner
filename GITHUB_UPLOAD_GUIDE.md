# GitHub Upload Guide - Universal SBOM Scanner

## Steps to Upload to GitHub

### 1. Initialize Git Repository (if not already done)

```bash
cd D:\Projects\SBOM
git init
```

### 2. Create .gitignore (if needed)

Already exists in the project. It excludes:
- Python cache files (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Output files (`*.json`, `*.xml`, `sbom-output/`)
- Build artifacts

### 3. Stage All Files

```bash
git add .
```

Or selectively add:
```bash
git add sbom_scanner/
git add examples/
git add *.md
git add *.txt
git add *.py
git add *.sh
git add *.ps1
git add LICENSE
```

### 4. Create Initial Commit

```bash
git commit -m "Initial commit: Universal SBOM Scanner v1.0.0

- Multi-language support (15 languages/platforms)
- JavaScript/TypeScript, Python, Java, PHP, .NET, Ruby, Rust, Go
- C/C++ (Conan, vcpkg, CMake)
- Embedded/IoT (PlatformIO, Arduino, Mbed OS)
- CycloneDX v1.5 output (JSON/XML)
- False positive reduction with confidence scoring
- CLI and programmatic API
- Cross-platform (Windows, Linux, macOS)
- Comprehensive documentation"
```

### 5. Create GitHub Repository

**Option A: Via GitHub Website**
1. Go to https://github.com/new
2. Repository name: `universal-sbom-scanner`
3. Description: `Multi-language SBOM generator supporting 15+ languages with CycloneDX output and minimal false positives`
4. Choose Public or Private
5. **DO NOT** initialize with README (we have one)
6. **DO NOT** add .gitignore or license (we have them)
7. Click "Create repository"

**Option B: Via GitHub CLI** (if installed)
```bash
gh repo create universal-sbom-scanner --public --description "Multi-language SBOM generator supporting 15+ languages with CycloneDX output" --source=.
```

### 6. Add Remote and Push

After creating the repo on GitHub, you'll see instructions. Run:

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/universal-sbom-scanner.git

# Or if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/universal-sbom-scanner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 7. Create Release (Optional but Recommended)

After pushing:

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `Universal SBOM Scanner v1.0.0`
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

---

## Complete Command Sequence

Here's the complete sequence to run in PowerShell:

```powershell
# Navigate to project
cd D:\Projects\SBOM

# Initialize git (if not done)
git init

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Initial commit: Universal SBOM Scanner v1.0.0

- Multi-language support (15 languages/platforms)
- JavaScript/TypeScript, Python, Java, PHP, .NET, Ruby, Rust, Go
- C/C++ (Conan, vcpkg, CMake)
- Embedded/IoT (PlatformIO, Arduino, Mbed OS)
- CycloneDX v1.5 output (JSON/XML)
- False positive reduction with confidence scoring
- CLI and programmatic API
- Cross-platform (Windows, Linux, macOS)
- Comprehensive documentation"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/universal-sbom-scanner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## GitHub Repository Configuration

### Repository Settings

**After uploading, configure these settings on GitHub:**

1. **About Section** (top right):
   - Description: "Multi-language SBOM generator with CycloneDX output"
   - Website: (add if you have documentation site)
   - Topics: `sbom`, `cyclonedx`, `security`, `dependencies`, `scanner`, `python`, `supply-chain`, `vulnerability-scanning`, `embedded`, `iot`

2. **Features to Enable**:
   - ✅ Issues
   - ✅ Discussions (recommended)
   - ✅ Projects (optional)
   - ✅ Wiki (optional)

3. **Branch Protection** (if making public):
   - Settings → Branches → Add rule for `main`
   - Enable: "Require pull request reviews before merging"

### GitHub Actions (Optional)

Create `.github/workflows/test.yml` for CI/CD:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run test script
      run: |
        python test_scanner.py
```

---

## What Gets Uploaded

### ✅ Included Files:
- `sbom_scanner/` - All source code (15 detectors + core)
- `examples/` - Example projects
- `*.md` - All documentation (README, USAGE, CONTRIBUTING, etc.)
- `requirements.txt` - Python dependencies
- `setup.py` - Package setup
- `LICENSE` - MIT license
- `test_scanner.py` - Test script
- `install.sh`, `install.ps1` - Installation scripts
- `.gitignore` - Git ignore rules

### ❌ Excluded Files (by .gitignore):
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python
- `venv/`, `env/` - Virtual environments
- `*.json`, `*.xml` - Generated SBOMs
- `.vscode/`, `.idea/` - IDE settings
- `build/`, `dist/` - Build artifacts

---

## Repository Description Template

**Short Description:**
```
Multi-language SBOM generator supporting 15+ languages with CycloneDX output and minimal false positives
```

**Full Description (for README on GitHub):**
```
🔍 Universal SBOM Scanner

A comprehensive multi-language Software Bill of Materials (SBOM) scanner that automatically 
detects and extracts dependencies from 15+ programming languages and platforms, generating 
industry-standard CycloneDX format output with minimal false positives.

✨ Features
• 15 language detectors (JS, Python, Java, C/C++, Go, Rust, PHP, Ruby, .NET, embedded)
• CycloneDX v1.5 output (JSON/XML)
• Confidence-based false positive reduction
• CLI and Python API
• Cross-platform support
• IoT/Embedded platform support (PlatformIO, Arduino, Mbed OS)
• Supply chain security ready

🚀 Perfect for security scanning, license compliance, CI/CD integration, and embedded systems!
```

---

## Post-Upload Checklist

After uploading to GitHub:

- [ ] Verify all files uploaded correctly
- [ ] Check README displays properly
- [ ] Add repository topics/tags
- [ ] Set up GitHub Actions (optional)
- [ ] Create v1.0.0 release
- [ ] Add badges to README (build status, license, etc.)
- [ ] Enable GitHub Discussions
- [ ] Add CONTRIBUTING.md to help contributors
- [ ] Star your own repo 😊
- [ ] Share on social media / dev communities

---

## Optional: Add Badges to README

Add these badges at the top of README.md:

```markdown
# Universal SBOM Scanner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CycloneDX](https://img.shields.io/badge/CycloneDX-1.5-green.svg)](https://cyclonedx.org/)
[![GitHub release](https://img.shields.io/github/release/YOUR_USERNAME/universal-sbom-scanner.svg)](https://github.com/YOUR_USERNAME/universal-sbom-scanner/releases)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/universal-sbom-scanner.svg?style=social)](https://github.com/YOUR_USERNAME/universal-sbom-scanner/stargazers)
```

---

## Troubleshooting

### Issue: Git not found
```bash
# Install Git for Windows: https://git-scm.com/download/win
```

### Issue: Authentication failed
```bash
# Use GitHub CLI or Personal Access Token
# Settings → Developer settings → Personal access tokens → Generate new token
```

### Issue: Large file warnings
```bash
# Check file sizes
git ls-files | xargs ls -lh | sort -k5 -hr | head -20

# Remove large files if needed
git rm --cached large-file.ext
echo "large-file.ext" >> .gitignore
```

### Issue: Merge conflicts
```bash
# Pull latest changes first
git pull origin main --rebase
git push origin main
```

---

## Next Steps

1. **Documentation Site**: Consider setting up GitHub Pages for docs
2. **PyPI Package**: Publish to PyPI for `pip install universal-sbom-scanner`
3. **Docker Image**: Create Dockerfile and push to Docker Hub
4. **GitHub Action**: Create GitHub Action for CI/CD integration
5. **Community**: Engage with users, respond to issues, accept PRs

---

**Ready to push to GitHub! 🚀**

Replace `YOUR_USERNAME` with your actual GitHub username in all commands above.

