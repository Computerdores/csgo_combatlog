# CS:GO Combat Log
Provides a command line combatlog with color coding for CS:GO.

Should work on all platforms, only tested for Windows.

# Setup
To work the CS:GO Game Client must be setup to support telnet, all that is required is adding the start option `-netconport <port>`. The Default port is `2121`, so to use the default it would be `-netconport 2121`.

If you want to change the port that is used (for example if the port is already in use) simply change the value of `PORT` variable in `csgo_combatlog.py`.