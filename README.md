# Coup_Discord_Bot
 A discord implementation of the card game coup.

## How to run
* You need to have python 3.5+ installed on your computer, and then install the [discord.py library](https://pypi.org/project/discord.py/)
```
pip install discord.py
```
* Create a Discord bot account, [heres a tutorial](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)
* Replace the API_KEY variable with your API key and run it.
I also put a list where you can add links that are sent to the winner (1 at a time randomly). In this file there is only one link but you can add more.
```python
#HERE IS WHERE YOU PUT YOUR API_KEY
API_KEY = ""

#List of links to pick from to send to winner
secret = ["https://i.kym-cdn.com/photos/images/newsfeed/001/193/375/5f7.jpeg", #smiley with sunglasses
]
```

## How to play
Coup is a fairly complicated game but you can find the rules [here](https://www.ultraboardgames.com/coup/game-rules.php)
You can play with up to six people.

*P.S.:* the rules are very slightly different from the original version.