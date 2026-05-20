#!/bin/bash

# Ensure we're in the app directory
cd /app

# Run the test specifically for the scheduler
npm test -- src/scheduler/Scheduler.test.js --watchAll=false

# Check exit code to determine reward
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
