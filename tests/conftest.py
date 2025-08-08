"""Pytest configuration for test suite.

Ensures the project root is on ``sys.path`` so that the ``controller`` module
and other top-level modules can be imported regardless of how pytest is
invoked.  Some environments execute the ``pytest`` entry point directly, which
does not automatically include the working directory on ``sys.path``.  Adding
this hook keeps the tests importable and mirrors typical development setups.
"""

import os
import sys

# Resolve the repository root and prepend it to sys.path if necessary.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

