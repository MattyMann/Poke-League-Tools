#!/bin/bash

FILES="*.html"

mkdir "records" &> /dev/null

for file in $FILES; do
	python process.py $file
	printf "$file processed\n"
	zpaq add "records/GameRecord.zpaq" $file -m5 &> /dev/null
	printf "$file backed up\n"
	rm $file
	printf "$file removed\n"
done

printf "\n"
rm -rf __pycache__
printf "Python cleaned up\n"
