#!/bin/bash
cat << 'EOF' > physics.py
def calculate_velocity(distance, time):
    if time == 0:
        return 0
    return distance / time
EOF
