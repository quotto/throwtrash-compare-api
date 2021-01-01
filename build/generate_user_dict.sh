#!/bin/bash

if [ $1 != "" ]; then
    /usr/lib/mecab/mecab-dict-index -d /usr/share/mecab/dic/ipadic -u $1 -f utf-8 -t utf-8 /build/user.csv
else
    echo "Missing distination filename"
    exit 1
fi