Files for managing the Pokemon league.

# Usage
To process HTML game files, simply move them into the same directory and run ```process.sh```. This will
- process the scores;
- add the results to the league table;
- update the elo rankings;
- and archive the matches.

# Roadmap
## Early to mid 2023
- [ ] Pokemon team & draft storage inc. cached storage of Pokemon data
- [ ] ~~Kill tracker on per-Pokemon basis~~ The kill tracker is much too difficult for me to implement. Damaging statuses, hazards, and time delayed moves (i.e. future sight), coupled with how Showdown stores the data mean it'd be a pretty hefty task to track kills. I don't think it's *impossible*, but I don't think I am capable of doing it.

## Late 2023
- [ ] ML analysis of mons, players, abilities, etc. to predict winners
- [ ] Interface for players to easily query aspects of the game inc. schedule, mons, utilities, etc.

## Stretch Goal
- [ ] Discord bots using this functionality as a backend
- [ ] GUI
