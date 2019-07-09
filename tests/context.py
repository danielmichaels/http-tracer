"""context helper module to allow unittests to import tracer package."""
import sys

import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
