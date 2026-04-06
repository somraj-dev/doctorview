import os
import sys

# Add the 'backend' directory to the Python path
path = os.path.join(os.path.dirname(__file__), 'backend')
if path not in sys.path:
    sys.path.append(path)

# Now we can import from the backend directory as if it were the root
from axiovital.wsgi import app
