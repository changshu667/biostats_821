#!/usr/bin/env bash

if [[ ! -f $1/esdb.md5 ]]; then
    echo "File does not exits, now continue to download md5 and save it under the 1st input file path"
    curl https://gitlab.oit.duke.edu/bios821/european_soccer_database/raw/master/esdb.md5 > $1/esdb.md5
    echo "md5 download completed"

else
    echo "File already exits, exit the process"
fi

md5fromfile=$(cut -b 1-32 $1/esdb.md5)
md5=$(md5sum $2/soccer.zip | cut -b 1-32)

echo "md5fromfile is" $md5fromfile
echo "md5 is" $md5

if [[ $md5fromfile = $md5 ]]; then
    echo "md5 and md5fromfile matches"
    if [[ -e $2/soccer.zip ]]; then
        echo "soccer.zip exists under the 2nd input file path and create a new folder called data under the path"
        mkdir $2/unzipped
        echo "move soccer.zip to the new folder"
        mv $2/soccer.zip $3
        echo "decompress soccer.zip"
        unzip $3/soccer.zip
    else
        echo "md5 and md5fromfile doesn't match"
        exit 3
    fi

else
    echo "md5sum does not match, exit the process"
    exit 4
fi
