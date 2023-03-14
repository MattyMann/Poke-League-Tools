echo "Which season are you creating?"
read SEASONNUM

echo "Please provide the name of a line-delimted file of player names"
read PLAYERS



echo "Is the following information correct?"
echo "Season: $SEASONNUM"
echo "Players:"
cat $PLAYERS

echo "Making season directory" && mkdir -p seasons/season_$SEASONNUM && echo "seasons/season_$SEASONNUM created"

