#!/bin/bash
echo "=== Starting Application ==="
echo "Python version:"
python --version
echo "Working directory:"
pwd
echo "Files:"
ls -la
echo "PORT env: $PORT"
echo "=== Starting Flask ==="
exec python main.py
