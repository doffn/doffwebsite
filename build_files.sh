#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Building project..."

# 1. Create a virtual environment in the build directory
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Upgrade pip inside the virtual environment
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run Django collection or migrations if needed
python manage.py collectstatic --noinput

echo "Build complete!"