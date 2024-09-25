# main.py located in the current directory
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mapping as map
map.ultrasonicToTwoDim()