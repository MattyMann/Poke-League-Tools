#!/bin/bash

while [[ $# -gt 0 ]]; do
	case $1 in
		-n)
			printf "Creating Season $2\n"
			SEASONDIR="seasons/season$2"
			mkdir -p "$SEASONDIR"
			printf "Created directory $SEASONDIR\n"
			python season_creator.py $2
			shift
		;;
	esac
	shift
done
