"""Production settings. Used by the GitHub Actions deploy.

    pelican content -s publishconf.py
"""

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: F401,F403

SITEURL = "https://rerooting.org"
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True
