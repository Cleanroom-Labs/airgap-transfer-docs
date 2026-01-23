# AirGap Transfer Documentation

Documentation for AirGap Transfer - a tool for transferring files to air-gapped systems.

## Building Documentation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build HTML documentation
make html

# Open in browser
open build/html/index.html
```

## Project Structure

```
airgap-transfer-docs/
├── source/
│   ├── index.rst              # Main documentation entry
│   ├── conf.py                # Sphinx configuration (imports shared theme)
│   ├── readme.rst             # Project overview
│   ├── roadmap.rst            # Implementation roadmap
│   ├── requirements/          # Software requirements
│   ├── design/                # Design documents
│   ├── testing/               # Test plans
│   ├── use-cases/             # Use case documentation
│   └── api/                   # API documentation
├── requirements.txt           # Python dependencies
├── Makefile                   # Build commands
└── README.md                  # This file
```

## Shared Theme

This documentation uses the shared Cleanroom Labs theme from `cleanroom-technical-docs/shared/theme-config.py`.

## Cross-Project References

To reference other AirGap projects:
- `:doc:`airgap-whisper:installation``
- `:doc:`airgap-deploy:usage``

## Resources

- [AirGap Transfer Overview](source/readme.rst)
- [Requirements Specification](source/requirements/srs.rst)
- [Design Document](source/design/sdd.rst)
- [Roadmap](source/roadmap.rst)
