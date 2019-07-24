#!/bin/bash

FLAG="$(cat flag.txt)"
FILENAME="flag.png"

pwgen -s 20 -n 1 > "key.txt"

python3 -c "import qrcode; qrcode.make('$FLAG').convert('RGB').save('$FILENAME')" && \
python3 "task.py" && \
echo "Done."
