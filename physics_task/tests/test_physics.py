import os
import sys
import json

sys.path.insert(0, '.')

def test_velocity():
    try:
        from physics import calculate_velocity
        assert calculate_velocity(10, 2) == 5
        assert calculate_velocity(0, 5) == 0
        score = 1.0
    except Exception as e:
        score = 0.0

    log_dir = os.environ.get('LOG_DIR', '/logs/verifier')
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'reward.json'), 'w') as f:
        json.dump({"score": score}, f)
