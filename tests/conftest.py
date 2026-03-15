import sys
import os

# Add the src/ folder to PYTHONPATH so pytest can find optimaai_uw
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
