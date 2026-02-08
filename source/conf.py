# Configuration file for AirGap Transfer documentation

import sys
import os

# Add common submodule to path
sys.path.insert(0, os.path.abspath('../common'))

# Import all shared settings
from theme_config import *

# Override default paths from theme_config.py for this project's layout
html_static_path = ['../common/sphinx/_static']
templates_path = ['../common/sphinx/_templates']
html_favicon = '../common/sphinx/_static/favicon.ico'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Project information -----------------------------------------------------

project = 'AirGap Transfer'
copyright = '2024, Cleanroom Labs'
author = 'Cleanroom Labs'
version = get_docs_version()
release = get_docs_version()

# -- sphinx-needs configuration ----------------------------------------------

needs_types = make_needs_types('TRANSFER-')

# -- Intersphinx configuration -----------------------------------------------

# Update intersphinx mapping with cross-project references
intersphinx_mapping.update({
    'cleanroom-whisper': ('https://cleanroomlabs.dev/docs/whisper/', None),
    'airgap-deploy': ('https://cleanroomlabs.dev/docs/deploy/', None),
})

# -- HTML output options -----------------------------------------------------

html_title = 'AirGap Transfer Documentation'
html_short_title = 'AirGap Transfer'

html_context = {
    'display_github': True,
    'github_user': 'cleanroom-labs',
    'github_repo': 'airgap-transfer-docs',
    'github_version': 'main',
    'conf_py_path': '/source/',
}
setup_project_icon(project, html_context)
setup_version_context(html_context)
