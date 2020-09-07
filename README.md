# rpg-helper-discord-bot
Bot for Discord RPG servers to basic help administration (like checking players active characters, statistics from channels)

# What is this?
Someday friend asked me for creating for him bot who can help him in manage of Discord server with a few weird functions which are needed only for "light" RPG servers.
Actually bot isn't used anywhere and probably never be used, but him source code is here. Feel free do what you want do.
* Repository is archived because I'm not planning maintain this
* If I correctly remember, code was rewritten to PEP8 standards 
* I used the`discord.py` package but the implementation for commands and async tasks is written by me (tho `discord.py` has custom packages to add support for these functions)

# What does this bot do?
* Look for players who have character but don't play (these players are on servers but doesn't do anything)
* Collects amount of messages on channels 
* Allows "write as bot" (you can also write messages in time delay without blocking bot)
* Running all of those functions in new asynchronous threads 
* Save settings and data in database
