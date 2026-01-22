#!/bin/bash

# Configuration
VENV_DIR=".venv"
SRC_DIR="src"
REQUIREMENTS="requirements.txt"
VERSION_FILE="$SRC_DIR/version.py"

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}--- Smart Display Launcher ---${NC}"

# 1. Check/Activate Virtual Environment
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "Error: Virtual environment '$VENV_DIR' not found."
    echo "Please create it using: python3 -m venv $VENV_DIR"
    exit 1
fi

# 2. Check Dependencies
if [ -f "$REQUIREMENTS" ]; then
    # Quietly install/update requirements
    pip install -q -r "$REQUIREMENTS"
fi

# 3. Get Version
VERSION="Unknown"
if [ -f "$VERSION_FILE" ]; then
    # Extract version string (robust enough for simple files)
    VERSION=$(grep "__version__" "$VERSION_FILE" | cut -d '"' -f 2)
fi

echo -e "Starting Application Version: ${GREEN}v$VERSION${NC}"
echo "------------------------------"

# 4. Run Application
# Using python directly on the file allows imports relative to the file location in sys.path
python "$SRC_DIR/app.py" "$@"
