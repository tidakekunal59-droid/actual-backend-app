#!/bin/bash

# Ensure output directory exists
mkdir -p /logs/verifier/

echo "Running tests using pytest..."

# Run pytest on the test_system.py file
python3 -m pytest /tests/test_system.py -v

# Check the exit status of pytest
if [ $? -eq 0 ]; then
    echo "1" > /logs/verifier/reward.txt
    echo "All tests passed successfully."
else
    echo "0" > /logs/verifier/reward.txt
    echo "Tests failed."
fi

exit 0
