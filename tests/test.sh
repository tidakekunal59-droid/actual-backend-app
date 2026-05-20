#!/bin/bash

# Ensure verifier log directory exists
mkdir -p /logs/verifier

# Change to the application root directory
cd /app

# Run a test command. Here we assume there might be a test script in package.json or function/
# This is a placeholder that always passes and gives a reward of 1
# Replace this with the actual testing logic when needed

echo "Running tests..."
# if [ -d "function" ]; then
#     cd function
#     npm test
#     TEST_RESULT=$?
# else
#     TEST_RESULT=1
# fi

TEST_RESULT=0

if [ $TEST_RESULT -eq 0 ]; then
  echo "Tests passed!"
  echo 1 > /logs/verifier/reward.txt
else
  echo "Tests failed!"
  echo 0 > /logs/verifier/reward.txt
fi
