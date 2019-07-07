#!/bin/bash

FLAG="$(cat flag.txt)"
FILENAME="flag.jpg"
BASE="Monolith_7D4.wav"

python3 -c "import qrcode; qrcode.make('$FLAG').convert('RGB').save('$FILENAME')" && \
./monolith "base/$BASE" -m $FILENAME && \
mv "mono/$FILENAME-#-$BASE-#-.mono" "flag.mono" && \
rm $FILENAME
echo "Done."
