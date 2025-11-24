#!/bin/bash
# Test script for interactive mode

cd /home/lbz/ai/AutoCodebase/.proj/PyRng
source venv/bin/activate

# Send commands to interactive mode
(
echo "show"
echo "set count 5"
echo "set distribution normal"
echo "set param.mu 0"
echo "set param.sigma 1"
echo "set seed 42"
echo "generate"
echo "exit"
) | pyrng --interactive
