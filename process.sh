#!/bin/bash

FILES="*.html"

for file in $FILES; do
	python process.py -q $file
	printf "$file processed\n"
	zpaq add "GameRecord.zpaq" $file -m5 &> /dev/null
	printf "$file backed up\n"
	rm $file
	printf "$file removed\n"
done

printf "\n"
rm -rf __pycache__
printf "Python cleaned up\n"
