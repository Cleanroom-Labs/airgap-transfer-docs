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
transfer/
├── common/                        # Submodule: shared design system & build tools
├── source/
│   ├── index.rst              # Main documentation entry
│   ├── conf.py                # Sphinx configuration (imports shared config)
│   ├── readme.rst             # Project overview
│   ├── roadmap.md             # Implementation roadmap
│   ├── requirements/          # Software requirements
│   ├── design/                # Design documents
│   ├── testing/               # Test plans
│   ├── use-cases/             # Use case documentation
│   └── api/                   # API documentation
├── requirements.txt           # References common/requirements.txt
├── Makefile                   # Build commands
└── README.md                  # This file
```

## Shared Theme

This documentation imports shared Cleanroom Labs configuration and styling from the submodule at `common/`.

## Cross-Project References

To reference other AirGap projects:
- `:doc:`cleanroom-whisper:readme``
- `:doc:`airgap-deploy:readme``

## Resources

- [AirGap Transfer Overview](source/readme.rst)
- [Requirements Specification](source/requirements/srs.rst)
- [Design Document](source/design/sdd.rst)
- [Roadmap](source/roadmap.md)
