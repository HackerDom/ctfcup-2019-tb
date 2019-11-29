#!/bin/bash

FLAG="flag.txt"
INPUT="container.wav"
OUTPUT="message.wav"

python2 "py_stego_phase/stego_phase.py" -i $INPUT -m $FLAG -o $OUTPUT
