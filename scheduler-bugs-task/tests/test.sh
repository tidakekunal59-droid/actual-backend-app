#!/bin/bash
mkdir -p /logs/verifier
cd /app
npm --version >/dev/null 2>&1
python3 -m pytest -q -s /tests/test_scheduler_pytest.py
status=$?
if [ $status -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
exit 0
