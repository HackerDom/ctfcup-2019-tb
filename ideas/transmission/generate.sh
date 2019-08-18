#!/bin/bash

FLAG="flag.txt"
ZIPNAME="docs.zip"
PASSWORD="$(cat password.txt)"

test -f $ZIPNAME && rm $ZIPNAME
zip -P$PASSWORD $ZIPNAME $FLAG
