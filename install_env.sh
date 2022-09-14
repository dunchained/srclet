#!/bin/sh

echo "Setting up venv..."
python3 -m venv venv
echo "Activating venv..."
source venv/bin/activate
echo "Done."
echo "Installing dependencies via pip..."
pip install -r requirements.txt
echo "Done."