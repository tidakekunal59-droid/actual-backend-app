#!/bin/bash
TASK_ID=$1
mkdir -p server/tests
cp tasks/$TASK_ID/task_tests.js server/tests/task_${TASK_ID}.test.js
cd server
npm test tests/task_${TASK_ID}.test.js
