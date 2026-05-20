#!/bin/bash

# Ensure we're in the app directory
cd /app

# Copy the test file into the source tree for verification
cp /tests/Scheduler.test.js src/scheduler/Scheduler.test.js

# Run the test specifically for the scheduler
npm test -- src/scheduler/Scheduler.test.js --watchAll=false

# Check exit code to determine reward
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

# Clean up test file
rm src/scheduler/Scheduler.test.js
