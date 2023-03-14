#!/bin/bash

# Rename the files into chronological order
FILES="*.html"

for file in $FILES; do
	TIMESTAMP=$(grep -oP '(?<=\|t:\|)([0-9]+)' -m 1 $file)
	mv $file "$TIMESTAMP.html"
	python process.py $file
	printf "$file processed\n"
	zpaq add "records/GameRecord.zpaq" $file -m5 &> /dev/null
	printf "$file backed up\n"
	rm $file
	printf "$file removed\n"
done

FILES="*.html"
for file in $FILES; do
	python process.py $file
	printf "$file processed\n"
	zpaq add "records/GameRecord.zpaq" $file -m5 &> /dev/null
	printf "$file backed up\n"
	rm $file
	printf "$file removed\n"
done
