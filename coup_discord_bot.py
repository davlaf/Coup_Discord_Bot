import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = "!") #sets what the commands start with

#HERE IS WHERE YOU PUT YOUR API_KEY
API_KEY = ""

#List of links to pick from to send to winner
secret = ["https://i.kym-cdn.com/photos/images/newsfeed/001/193/375/5f7.jpeg", #smiley with sunglasses
]

validcards = ["contessa","capitaine","duc","assassin","ambassadeur",]
class player:
    def __init__(self,context):
        self.coins = 2
        self.carddisplay = []
        self.cards = [] #array len 2 of strings
        self.shown = [False,False]
        self.isalive = True
        self.context = context
        self.name = context.author.name

    async def removecard(self, ctx):
        global aliveplayers
        if (self.shown[0] or self.shown[1]): #just kill him
            print (f"{self.name} has died!")
            self.shown[0] = True
            self.shown[1] = True
            self.cards.clear()
            self.isalive = False
            aliveplayers -= 1
            if (aliveplayers > 1):
                print(f"{self.name} has died. {aliveplayers} players remain in the game.")
                await ctx.send(f"{self.name} has died. {aliveplayers} players remain in the game.")
            else:
                print(f"{self.name} has died.")
                await ctx.send(f"{self.name} has died.")
        else: # give player choice
            await ctx.send(f"{self.name}, say !show and which one of your cards you want to show.")
            while True:
                def checkshow(m):
                    return m.content.startswith("!show ") and m.author.name == self.name and m.channel == ctx.channel
                print(f"waiting for {self.name} to say which card he wants to show...")
                msg = await client.wait_for('message', check=checkshow)
                if (msg.content[6:].lower() in validcards):
                    if (msg.content[6:].capitalize() in self.cards):
                        self.shown[self.cards.index(msg.content[6:].capitalize())] = True
                        self.cards.remove(msg.content[6:].capitalize())
                        await ctx.send(f"{self.name} has shown {msg.content[6:].capitalize()}.")
                        print (f"{self.name} has shown {msg.content[6:].capitalize()}.")
                        break
                    else:
                        await ctx.send(f"{self.name}, you don't have {msg.content[6:].capitalize()}.")
                else:
                    await ctx.send(f"{self.name}, {msg.content[6:]} is not a valid card! Valid cards are Ambassadeur, Assassin, Capitaine, Contessa and Duc.")

    async def steal(self, ctx, victim):
        if (players[playernames.index(victim)].coins == 1):
            players[playernames.index(victim)].coins = 0
            self.coins += 1
            await ctx.send(f"{self.name} has taken 1 coin from {victim}.")
            print(f"{self.name} has taken 1 coin from {victim}.")
        elif (players[playernames.index(victim)].coins >= 2):
            players[playernames.index(victim)].coins -= 2
            self.coins += 2
            await ctx.send(f"{self.name} has taken 2 coins from {victim}.")
            print(f"{self.name} has taken 2 coin from {victim}.")

    async def bluffcardchange(self,ctx,card):
        cardchoice = []
        if (card != "none"):
            cardchoice.append(self.cards[self.cards.index(card)])
        else:
            cardchoice.append(self.cards[0])
        cardchoice.append(cards.pop(len(cards)-1))
        cardchoice.append(cards.pop(len(cards)-2))
        await self.context.author.send(f"Choose 1 card to keep between {listarray(cardchoice)} using !keep <card>")
        while True:
            def checkcardselect(m):
                return m.content.startswith("!keep") and m.author.name == self.name and m.channel != ctx.channel
            print(f"waiting for {self.name} to say which card he wants to keep after {'playing ambassadeur' if card == 'none' else 'being called bluff on when he wasnt bluffing'}...")
            msg = await client.wait_for('message', check=checkcardselect)
            if (len(msg.content.split(" ")) == 2):
                if (msg.content.split(" ")[1].lower() in validcards):
                    if (msg.content.split(" ")[1].capitalize() in cardchoice):
                        #put cards he chose in his .cards and the rest at the bottom of the deck
                        if (card != "none"):
                            if (self.shown[0] or self.shown[1]):
                                self.cards = [cardchoice.pop(cardchoice.index(msg.content.split(" ")[1].capitalize()))]
                                if (msg.content.split(" ")[1].capitalize() == card):
                                    print(f"{self.name} kept {card}.")
                                else:
                                    print(f"{self.name} switched {card} for {msg.content.split(' ')[1].capitalize()}.")
                                if (self.shown[0]):
                                    self.carddisplay[1] = self.cards[0]
                                elif (self.shown[1]):
                                    self.carddisplay[0] = self.cards[0]
                            else:
                                index = self.cards.index(card)
                                self.cards[index] = cardchoice.pop(cardchoice.index(msg.content.split(" ")[1].capitalize()))
                                self.carddisplay[self.carddisplay.index(card)] = self.cards[index]
                        else:
                            self.cards = [cardchoice.pop(cardchoice.index(msg.content.split(" ")[1].capitalize()))]
                            if (self.shown[0]):
                                self.carddisplay[1] = self.cards[0]
                            elif (self.shown[1]):
                                self.carddisplay[0] = self.cards[0]
                        if (len(self.cards) == 1):
                            await self.context.author.send(f"Your card is now {self.cards[0]}.")
                            print(f"{self.name}\'s card is now {self.cards[0]}")
                        else:
                            await self.context.author.send(f"Your cards are now {self.cards[0]} and {self.cards[1]}.")
                            print(f"{self.name}\'s cards are now {self.cards[0]} and {self.cards[1]}.")
                        random.shuffle(cardchoice)
                        cards.insert(0,cardchoice[0])
                        cards.insert(0,cardchoice[1])
                        break
                    else:
                        await self.context.author.send(f"{msg.content.split(' ')[1]} is not a card you can choose! Choose 1 card to keep between {listarray(cardchoice)}.")
                else:
                    await self.context.author.send(f"{msg.content.split(' ')[1]} is not a valid card.")
            else:
                await self.context.author.send(f"You used the command incorrectly! Say !keep <card> where \"<card>\" is replaced by the card you want to keep.")


    async def ambassadeur(self, ctx):
        global cards
        await ctx.send(f"{playernames[currentplayer]}, check your DMs to choose your cards using Ambassadeur.")
        cardchoice = []
        if (len(self.cards) == 2):
            oldcards = [self.cards[0],self.cards[1]]
            cardchoice.append(self.cards.pop(0))
            cardchoice.append(self.cards.pop(0))
            cardchoice.append(cards.pop(len(cards)-1))
            cardchoice.append(cards.pop(len(cards)-1))
            await self.context.author.send(f"Choose 2 cards to keep between {listarray(cardchoice)} using !keep <card> <card>")
            while True:
                def checkcardselect(m):
                    return m.content.startswith("!keep") and m.author.name == self.name and m.channel != ctx.channel
                print(f"waiting for {self.name} to pick which 2 cards he wants for ambassadeur...")
                msg = await client.wait_for('message', check=checkcardselect)
                if (len(msg.content.split(" ")) == 3): #input checking is boring please could someone help me
                    if (msg.content.split(" ")[1].lower() in validcards):
                        if (msg.content.split(" ")[2].lower() in validcards):
                            if (msg.content.split(" ")[1].capitalize() in cardchoice):
                                if (msg.content.split(" ")[2].capitalize() in cardchoice):
                                    if (msg.content.split(" ")[1].capitalize() == msg.content.split(" ")[2].capitalize()):
                                        if (cardchoice.count(msg.content.split(" ")[1].capitalize()) > 1):
                                            #put cards he chose in his .cards and the rest at the bottom of the deck
                                            self.cards = [cardchoice.pop(cardchoice.index(msg.content.split(" ")[1].capitalize())), cardchoice.pop(cardchoice.index(msg.content.split(" ")[2].capitalize()))]
                                            """
                                            print(f"{self.name} chose to keep two {msg.content.split(' ')[2]}.")
                                            messageadder = f"{self.name} "
                                            if (self.cards[0] in oldcards):
                                                messageadder += f"kept his {self.cards[0]} and "
                                            else:
                                                messageadder += f"changed his {oldcards.pop(0)} for {self.cards[0]} and "
                                            if (self.cards[1] in oldcards):
                                                messageadder += f"kept his {oldcards[0]}."
                                            else:
                                                messageadder += f"changed his {self.cards[1]} for {oldcards[0]}."
                                            print(messageadder)
                                            """
                                            self.carddisplay = [self.cards[0],self.cards[1]]
                                            random.shuffle(cardchoice)
                                            cards.insert(0,cardchoice[0])
                                            cards.insert(0,cardchoice[1])
                                            await self.context.author.send(f"Your cards are now {self.cards[0]} and {self.cards[1]}.")
                                            print(f"{self.name}\'s cards are now {self.cards[0]} and {self.cards[1]}.")
                                            break
                                        else:
                                            await self.context.author.send(f"There aren't 2 {msg.content.split(' ')[1]} in the list of cards you can choose!")
                                    else:
                                        #put cards he chose in his .cards and the rest at the bottom of the deck
                                        self.cards = [cardchoice.pop(cardchoice.index(msg.content.split(" ")[1].capitalize())), cardchoice.pop(cardchoice.index(msg.content.split(" ")[2].capitalize()))]
                                        """
                                        messageadder = f"{self.name} "
                                        if (self.cards[0] in oldcards):
                                            messageadder += f"kept his {self.cards[0]} and "
                                        else:
                                            messageadder += f"changed his {oldcards.pop(oldcards.index(self.cards[0]))} for {self.cards[0]} and "
                                        if (self.cards[1] in oldcards):
                                            messageadder += f"kept his {oldcards[0]}."
                                        else:
                                            messageadder += f"changed his {self.cards[1]} for {oldcards[0]}."
                                        print(messageadder)
                                        """
                                        self.carddisplay = [self.cards[0],self.cards[1]]
                                        self.carddisplay = [self.cards[0],self.cards[1]]
                                        random.shuffle(cardchoice)
                                        cards.insert(0,cardchoice[0])
                                        cards.insert(0,cardchoice[1])
                                        if (len(self.cards) == 1):
                                            await self.context.author.send(f"Your card is now {self.cards[0]}.")
                                            print(f"{self.name}\'s card is now {self.cards[0]}")
                                        else:
                                            await self.context.author.send(f"Your cards are now {self.cards[0]} and {self.cards[1]}.")
                                            print(f"{self.name}\'s cards are now {self.cards[0]} and {self.cards[1]}.")
                                        break
                                else:
                                    await self.context.author.send(f"{msg.content.split(' ')[2]} is not a card you can choose! Choose 2 cards to keep between {listarray(cardchoice)}.")
                            else:
                                await self.context.author.send(f"{msg.content.split(' ')[1]} is not a card you can choose! Choose 2 cards to keep between {listarray(cardchoice)}.")
                        else:
                            await self.context.author.send(f"{msg.content.split(' ')[2]} is not a valid card.")
                    else:
                        await self.context.author.send(f"{msg.content.split(' ')[1]} is not a valid card.")
                else:
                    await self.context.author.send(f"You used the command incorrectly! Say !keep <card> <card> where \"<card>\" is replaced by the cards you want to keep.")
        else:
            await self.bluffcardchange(ctx,"none")


def reset():
    global gamestate
    global players
    global turn
    global playernames
    global currentplayer
    global aliveplayers
    global cards
    cards = ["Contessa","Contessa","Contessa",
             "Capitaine","Capitaine","Capitaine",
             "Duc","Duc","Duc",
             "Assassin","Assassin","Assassin",
             "Ambassadeur","Ambassadeur","Ambassadeur"]
    gamestate = "notrunning"
    players = []
    playernames = []
    turn = 0
    currentplayer = 0
    aliveplayers = 0

reset()

def listarray(array):
    list = ""
    for i in range(0,len(array)):
        if (i == len(array)-2):
            list += str(array[i]) + " and "
        elif (i == len(array)-1):
            list += str(array[i])
        else:
            list += str(array[i]) + ", "
    return list

async def game(ctx):
    print ("Game starting!")
    #global numalive
    global gamestate
    global turn
    global currentplayer
    await ctx.send(f"Starting coup with {listarray(playernames)}")
    #numalive = len(players)
    gamestate = "player turn"
    random.shuffle(cards)
    print(f"The cards in the deck are (bottom to top) {listarray(cards)}")
    for i in players:
        #Picks 2 cards from top of deck
        i.cards = [cards.pop(len(cards)-1),cards.pop(len(cards)-2)]
        i.carddisplay += i.cards
        await (i.context.author).send(f"You have {i.cards[0]} and {i.cards[1]}.")
        print(f"{i.name} has {i.cards[0]} and {i.cards[1]}.")
    await ctx.send("Cards have been sent! Check your DMs.")
    while gamestate != "notrunning":
        if (aliveplayers == 1):
            gamestate = "notrunning"
            break
        #start of turn
        await ctx.send(f"Turn {turn+1}: {playernames[currentplayer]}")
        print (f"Turn {turn+1}.")
        cardstring = ""
        devstring = "\n"
        for i in players: #displays player information
            cardstring += f"{i.name}: Cards: "
            devstring += f"{i.name}: Cards: "
            if (i.shown[0]):
                cardstring += str(i.carddisplay[0])
                devstring += str(i.carddisplay[0])
            else:
                cardstring += "▓▓▓▓▓▓"
                devstring += f"({str(i.carddisplay[0])})"
            cardstring += " et "
            devstring += " et "
            if (i.shown[1]):
                cardstring += str(i.carddisplay[1])
                devstring += str(i.carddisplay[1])
            else:
                cardstring += "▓▓▓▓▓▓"
                devstring += f"({str(i.carddisplay[1])})"
            if (i.isalive):
                cardstring += f" Coins: {i.coins} \n"
                devstring += f" Coins: {i.coins}"
                if (i != players[len(players)-1]):
                    devstring += "\n"
            else:
                cardstring += " (Dead)\n"
                devstring += " (Dead)"
                if (i != players[len(players)-1]):
                    devstring += "\n"
        await ctx.send(cardstring)
        print(devstring+"\n")
        lastmove = ""
        if (players[currentplayer].coins < 10):
            while True: #wait until players says a valid input
                def checkplay(m):
                    return m.author == players[currentplayer].context.author and m.channel == ctx.channel and (m.content.startswith("!play ") or m.content == "!coin" or m.content == "!aid" or m.content.startswith("!coup"))
                print(f"waiting for {players[currentplayer]} to do an action...")
                msg = await client.wait_for('message', check=checkplay)
                if (msg.content.startswith("!coup")):
                    if (len(msg.content.split(" ")) != 1):
                        if (msg.content[6:] != msg.author.name):
                            if (players[currentplayer].coins >= 7):
                                if (msg.content[6:] in playernames):
                                    if (players[playernames.index(msg.content[6:])].isalive):
                                        lastmove = "coup"
                                        break
                                    else:
                                        await ctx.send(f"You can't coup {msg.content[6:]} because he is dead!")
                                else:
                                    await ctx.send(f"\"{msg.content[6:]}\" is not a player! Valid players are {listarray(playernames)}.")
                            else:
                                await ctx.send("You don't have enough coins to use coup!")
                        else:
                            await ctx.send("You can't coup yourself!")
                    else:
                        await ctx.send("You need to specify a target! Usage: !coup <playername>")
                elif (msg.content == "!coin"):
                    lastmove = "coin"
                    break
                elif (msg.content == "!aid"):
                    lastmove = "aid"
                    break
                elif (msg.content[6:].lower() == "contessa"):
                    print(f"{msg.author.name} tried to play Contessa.")
                    if (players[currentplayer].coins < 3):
                        await ctx.send("You can't currently play Contessa. Valid cards are Ambassadeur, Capitaine and Duc.")
                    else:
                        await ctx.send("You can't currently play Contessa. Valid cards are Ambassadeur, Assassin, Capitaine and Duc.")
                elif (msg.content[6:14].lower() == "assassin"):
                    if (len(msg.content.split(" ")) != 2): #checks if person inputed something
                        if (msg.content[15:] != msg.author.name): #checks if it isnt the author's name
                            if (players[currentplayer].coins >= 3):
                                if (msg.content[15:] in playernames): #checks if it is a name
                                    if (players[playernames.index(msg.content[15:])].isalive):
                                        lastmove = "Assassin"
                                        target = msg.content[15:]
                                        aggressor = msg.author.name
                                        players[currentplayer].coins -= 3
                                        break
                                    else:
                                        await ctx.send(f"You can't assassinate {msg.content[15:]} because he is dead!")
                                else:
                                    await ctx.send(f"\"{msg.content[15:]}\" is not a player! Valid players are {listarray(playernames)}.")
                            else:
                                await ctx.send("You don't have enough coins to play Assassin! Valid cards are Ambassadeur, Capitaine and Duc.")
                        else:
                            await ctx.send("You can't assassinate yourself!")
                    else:
                        await ctx.send("You need to specify a target! !play Assassin <playername>")
                elif (msg.content[6:15].lower() == "capitaine"):
                    if (msg.content[6:].lower().rstrip() != "capitaine"): #checks if person input something
                        if (msg.content[16:] in playernames): #checks if it is a name
                            if (msg.content[16:] != msg.author.name): #checks if it isnt the author's name
                                if (players[playernames.index(msg.content[16:])].isalive):
                                    if (players[playernames.index(msg.content[16:])].coins > 0): #checks if the target has enough coins
                                        lastmove = "Capitaine"
                                        target = msg.content[16:]
                                        aggressor = msg.author.name
                                        break
                                    else:
                                        await ctx.send(f"You can't steal from {msg.content[16:]} because he has no coins!")
                                else: # if he has 0 coins
                                    await ctx.send(f"You can't steal from {msg.content[16:]} because he is dead.")
                            else:
                                await ctx.send("You can't steal from yourself!")
                        else:
                            await ctx.send(f"\"{msg.content[16:]}\" is not a player! Valid players are {listarray(playernames)}.")
                    else:
                        await ctx.send("You need to specify a target! !play Capitaine <playername>")

                elif (msg.content[6:].lower() == "ambassadeur"):
                    lastmove = "Ambassadeur"
                    break
                elif (msg.content[6:].lower() == "duc"):
                    lastmove = "Duc"
                    break
                else:
                    print(f"{msg.author.name} played an invalid card")
                    if (players[currentplayer].coins < 3):
                        await ctx.send(f"\"{msg.content[6:]}\" is not a card! Valid cards are Ambassadeur, Capitaine and Duc.")
                    else:
                        await ctx.send(f"\"{msg.content[6:]}\" is not a card! Valid cards are Ambassadeur, Assassin, Capitaine and Duc.")
            if (lastmove != "coin" and lastmove != "aid" and lastmove != "coup"):
                if (msg.content.split(" ")[1].capitalize() in players[currentplayer].cards):
                    print(f"{msg.author.name} played {msg.content.split(' ')[1].capitalize()}.")
                else:
                    print(f"{msg.author.name} bluffed {msg.content.split(' ')[1].capitalize()}.")
            if (lastmove == "coup"):
                players[currentplayer].coins -= 7
                await ctx.send(f"{players[currentplayer].name} used coup on {msg.content[6:]}!")
                print(f"{players[currentplayer].name} used coup on {msg.content[6:]}!")
                await players[playernames.index(msg.content[6:])].removecard(ctx)
                if (aliveplayers == 1):
                    gamestate = "notrunning"
                    break
            elif (lastmove == "coin"):
                print(f"{playernames[currentplayer]} took 1 coin.")
                await ctx.send(f"{playernames[currentplayer]} took 1 coin.")
                players[currentplayer].coins += 1
            elif (lastmove == "aid"):
                await ctx.send(f"{playernames[currentplayer]} wants foreign aid. Say !ok to keep playing or !block if you have Duc.")
                print(f"{playernames[currentplayer]} wants foreign aid.")
                okplayers = []
                while True:
                    def checkokorblock(m):
                        return m.author.name != playernames[currentplayer] and m.channel == ctx.channel and (m.content == "!ok" or m.content == "!block")
                    print(f"waiting for someone to block {playernames[currentplayer]} from getting foreign aid or for everyone to say !ok...")
                    msg = await client.wait_for("message", check=checkokorblock)
                    if (msg.content == "!block"):
                        if ("Duc" in players[playernames.index(msg.author.name)].cards):
                            print(f"{msg.author.name} blocked by playing Duc.")
                        else:
                            print(f"{msg.author.name} blocked by bluffing Duc.")
                        await ctx.send(f"{msg.author.name} has blocked {playernames[currentplayer]} from obtaining foreign aid using Duc. {playernames[currentplayer]}, say !ok to keep playing or !bluff to call bluff.")
                        def checkblufforok(m):
                            return m.author.name == playernames[currentplayer] and m.channel == ctx.channel and (m.content == "!ok" or m.content == "!bluff")
                        print(f"waiting for {playernames[currentplayer]} to say !ok or call !bluff on {msg.author.name}...")
                        blockmsg = await client.wait_for("message", check=checkblufforok)
                        if (blockmsg.content == "!ok"):
                            await ctx.send(f"{msg.author.name} has blocked {playernames[currentplayer]} from getting foreign aid.")
                            print(f"{playernames[currentplayer]} accepts the block.")
                            break
                        else: #if its !bluff
                            if ("Duc" in players[playernames.index(msg.author.name)].cards): #if target has the card
                                print(f"{playernames[currentplayer]} called bluff incorrectly.")
                                await ctx.send(f"{msg.author.name} wasn't bluffing!")
                                await players[currentplayer].removecard(ctx)
                                if (aliveplayers == 1):
                                    gamestate = "notrunning"
                                    break
                                await ctx.send(f"{msg.author.name}, check your DMs to keep or change your card.")
                                await players[playernames.index(msg.author.name)].bluffcardchange(ctx,"Duc")
                                break
                            else: #if target was bluffing
                                print(f"{playernames[currentplayer]} called bluff correctly.")
                                await ctx.send(f"{msg.author.name} was bluffing!")
                                await players[playernames.index(msg.author.name)].removecard(ctx)
                                if (aliveplayers == 1):
                                    gamestate = "notrunning"
                                    break
                                await ctx.send(f"{playernames[currentplayer]} took 2 coins.")
                                print(f"{playernames[currentplayer]} gets 2 coins.")
                                players[currentplayer].coins += 2
                                break
                    if (not msg.author.name in okplayers): #if message was ok
                        okplayers.append(msg.author.name)
                        print(f"{msg.author.name} doesn't block.")
                    if (len(okplayers) == aliveplayers-1):
                        print(f"No one blocked {playernames[currentplayer]} from getting foreign aid. {playernames[currentplayer]} takes 2 coins.")
                        await ctx.send(f"No one blocked {playernames[currentplayer]} from getting foreign aid. {playernames[currentplayer]} takes 2 coins.")
                        players[currentplayer].coins += 2
                        break
            elif (lastmove == "Capitaine" or lastmove == "Assassin"):
                if (lastmove == "Capitaine"):
                    print(f"{msg.author.name} used Capitaine on {target}.")
                    await ctx.send(f"{target}, {msg.author.name} used Capitaine on you. Say !ok to keep playing, !bluff to call bluff or !block <card> if you have Ambassadeur or Capitaine.")
                else: #if its assassin
                    print(f"{msg.author.name} used Assassin on {target}. -3 coins for {msg.author.name}.")
                    await ctx.send(f"{target}, {msg.author.name} used Assassin on you. -3 coins for {msg.author.name}. Say !ok to keep playing, !bluff to call bluff or !block if you have Contessa.")
                while True:
                    def checkblufforokorblock(m):
                        return m.author.name == target and m.channel == ctx.channel and (m.content == "!ok" or m.content == "!bluff" or m.content.startswith("!block"))
                    print(f"waiting for {target} to say !ok or !bluff or !block...")
                    msg = await client.wait_for("message", check=checkblufforokorblock)
                    if (msg.content.startswith("!block")):
                        if (lastmove == "Capitaine"):
                            if (len(msg.content.split(' ')) == 2):
                                if (msg.content.split(' ')[1].lower() in validcards):
                                    if (msg.content.split(' ')[1].lower() == "capitaine" or msg.content.split(' ')[1].lower() == "ambassadeur"):
                                        if (msg.content.split(' ')[1].lower() in players[playernames.index(msg.author.name)].cards):
                                            print(f"{msg.author.name} blocked by playing {msg.content.split(' ')[1].lower()}.")
                                        else:
                                            print(f"{msg.author.name} blocked by bluffing {msg.content.split(' ')[1].lower()}.")
                                        await ctx.send(f"{target} has blocked {aggressor}\'s Capitaine using {msg.content.split(' ')[1].capitalize()}! {aggressor}, say !ok to keep playing or !bluff to call bluff.")
                                        targetblockcard = msg.content.split(' ')[1].capitalize()
                                        def checkblufforok(m):
                                            return m.author.name == aggressor and m.channel == ctx.channel and (m.content == "!ok" or m.content == "!bluff")
                                        print(f"waiting for {aggressor} to say !ok or !bluff on {target}'s bluff...")
                                        blockmsg = await client.wait_for("message", check=checkblufforok)
                                        if (blockmsg.content == "!ok"):
                                            await ctx.send(f"{target} has blocked {aggressor}\'s Capitaine using {targetblockcard}.")
                                            print(f"{aggressor} accepted the block.")
                                            break
                                        else: #if its !bluff
                                            if (targetblockcard in players[playernames.index(target)].cards): #if target has the card
                                                await ctx.send(f"{target} wasn't bluffing!")
                                                print(f"{aggressor} called bluff incorrectly.")
                                                await players[currentplayer].removecard(ctx)
                                                if (aliveplayers == 1):
                                                    gamestate = "notrunning"
                                                    break
                                                await ctx.send(f"{target}, check your DMs to keep or change your card.")
                                                await players[playernames.index(target)].bluffcardchange(ctx,targetblockcard)
                                                break
                                            else: #if target was bluffing
                                                await ctx.send(f"{target} was bluffing!")
                                                print(f"{aggressor} called bluff correctly.")
                                                await players[playernames.index(target)].removecard(ctx)
                                                if (aliveplayers == 1):
                                                    gamestate = "notrunning"
                                                    break
                                                await players[currentplayer].steal(ctx,target)
                                                break
                                    else:
                                        await ctx.send(f"{msg.content.split(' ')[1].capitalize()} cannot be used to block Capitaine! Valid cards are Ambassadeur and Capitaine.")
                                else:
                                    await ctx.send(f"\"{msg.content.split(' ')[1]}\" is not a valid card! Valid cards are Ambassadeur and Capitaine.")
                            else:
                                await ctx.send("Invalid use of !block. Usage: !block <card> where \"<card>\" is replaced by Ambassadeur or Capitaine.")
                        elif (lastmove == "Assassin"): #if last move was assassin
                            await ctx.send(f"{target} has blocked {aggressor}\'s Assassin using Contessa! {aggressor}, say !ok to keep playing or !bluff to call bluff.")
                            if ("Contessa" in players[playernames.index(target)].cards):
                                print(f"{msg.author.name} blocked by playing Contessa.")
                            else:
                                print(f"{msg.author.name} blocked by bluffing Contessa.")
                            def checkblufforok(m):
                                return m.author.name == aggressor and m.channel == ctx.channel and (m.content == "!ok" or m.content == "!bluff")
                            print(f"waiting for {aggressor} to call bluff or say !ok to {target}'s block...")
                            blockmsg = await client.wait_for("message", check=checkblufforok)
                            if (blockmsg.content == "!ok"):
                                await ctx.send(f"{target} has blocked {aggressor}\'s Assassin using Contessa.")
                                print(f"{aggressor} accepted the block.")
                                break
                            else: #if its !bluff
                                if ("Contessa" in players[playernames.index(target)].cards): #if target has the card
                                    await ctx.send(f"{target} wasn't bluffing!")
                                    await players[currentplayer].removecard(ctx)
                                    if (aliveplayers == 1):
                                        gamestate = "notrunning"
                                        break
                                    await ctx.send(f"{target}, check your DMs to keep or change your card.")
                                    await players[playernames.index(target)].bluffcardchange(ctx,"Contessa")
                                    break
                                else: #if target was bluffing
                                    await ctx.send(f"{target} was bluffing!")
                                    players[playernames.index(target)].shown[0] = True
                                    await players[playernames.index(target)].removecard(ctx)
                                    if (aliveplayers == 1):
                                        gamestate = "notrunning"
                                        break
                                    break
                    else: #if it is not !ok or !bluff, dont loop it.
                        break
                if (msg.content == "!ok"):
                    await ctx.send(f"{target} doesn't call bluff.")
                    if (lastmove == "Capitaine"):
                        await players[currentplayer].steal(ctx,target)
                    else: #if it was assassin
                        await ctx.send(f"{aggressor} used Assassin on {target}")
                        await players[playernames.index(target)].removecard(ctx)
                        if (aliveplayers == 1):
                            gamestate = "notrunning"
                            break
                elif (msg.content == "!bluff"):
                    if (lastmove in players[currentplayer].cards): #if person has the card
                        await ctx.send(f"{playernames[currentplayer]} wasn't bluffing!")
                        if (lastmove == "Assassin"):
                            players[playernames.index(target)].shown[0] = True
                        await players[playernames.index(target)].removecard(ctx)
                        if (aliveplayers == 1):
                            gamestate = "notrunning"
                            break
                        await ctx.send(f"{playernames[currentplayer]}, check your DMs to keep or change your card.")
                        await players[currentplayer].bluffcardchange(ctx,lastmove)
                    else: #if the person was bluffing
                        await ctx.send(f"{playernames[currentplayer]} was bluffing!")
                        await players[currentplayer].removecard(ctx)
                        if (aliveplayers == 1):
                            gamestate = "notrunning"
                            break
            else: #duc or ambassadeur
                await ctx.send(f"{msg.author.name} played {lastmove}. Say !ok to keep playing or !bluff to call bluff.")
                okplayers = []
                while True: #get everyone to say !ok or have someone call bluff
                    def checkblufforok(m):
                        return m.author.name != playernames[currentplayer] and m.channel == ctx.channel and (m.content == "!ok" or m.content == "!bluff")
                    print(f"waiting for everyone except {playernames[currentplayer]} to call bluff...")
                    msg = await client.wait_for('message', check=checkblufforok)
                    if (msg.content == "!bluff"):
                        if (players[playernames.index(msg.author.name)].isalive): #if person is alive
                            if (lastmove in players[currentplayer].cards): #if person has the card
                                await ctx.send(f"{playernames[currentplayer]} wasn't bluffing!")
                                await players[playernames.index(msg.author.name)].removecard(ctx)
                                if (aliveplayers == 1):
                                    gamestate = "notrunning"
                                    break
                                if (lastmove == "Duc"):
                                    await ctx.send(f"{playernames[currentplayer]} gets 3 coins.")
                                    players[currentplayer].coins += 3
                                    await ctx.send(f"{playernames[currentplayer]}, check your DMs to keep or change your card.")
                                    await players[currentplayer].bluffcardchange(ctx,lastmove)
                                elif (lastmove == "Ambassadeur"):
                                    await players[currentplayer].ambassadeur(ctx)
                                break
                            else: #if the person was bluffing
                                await ctx.send(f"{playernames[currentplayer]} was bluffing!")
                                await players[currentplayer].removecard(ctx)
                                if (aliveplayers == 1):
                                    gamestate = "notrunning"
                                    break
                                break
                        else:
                            await ctx.send(f"{msg.author.name}, dead players can't call bluff!")
                    elif (not msg.author.name in okplayers): #if message was ok
                        if (msg.author.name in playernames): #if person is alive
                            if (players[playernames.index(msg.author.name)].isalive): #if person is alive
                                okplayers.append(msg.author.name)
                                print(f"{msg.author.name} doesn't call bluff")
                            else:
                                await ctx.send(f"{msg.author.name}, dead players can't say ok!")
                        else:
                            await ctx.send(f"{msg.author.name}, you aren't in the game!")
                    if (len(okplayers) == aliveplayers-1):
                        print(f"No one called bluff.")
                        await ctx.send("No one called bluff.")
                        if (lastmove == "Duc"):
                            await ctx.send(f"{playernames[currentplayer]} gets 3 coins.")
                            players[currentplayer].coins += 3
                        elif (lastmove == "Ambassadeur"):
                            await players[currentplayer].ambassadeur(ctx)
                        break
        else:
            await ctx.send(f"{playernames[currentplayer]}, because you have more than 10 coins you have to use coup on someone. Say !coup <player> to use coup.")
            print(f"{playernames[currentplayer]} has 10 or more coins so he has to coup someone.")
            while True:
                def checkplay(m):
                    return m.author == players[currentplayer].context.author and m.channel == ctx.channel and m.content.startswith("!coup")
                print(f"waiting for {playernames[currentplayer]} to forcefully coup someone...")
                msg = await client.wait_for('message', check=checkplay)
                if (msg.content.startswith("!coup")):
                    if (len(msg.content.split(" ")) != 1):
                        if (msg.content[6:] != msg.author.name):
                            if (players[currentplayer].coins >= 7):
                                if (msg.content[6:] in playernames):
                                    if (players[playernames.index(msg.content[6:])].isalive):
                                        players[currentplayer].coins -= 7
                                        await ctx.send(f"{players[currentplayer].name} used coup on {msg.content[6:]}!")
                                        print(f"{players[currentplayer].name} used coup on {msg.content[6:]}!")
                                        await players[playernames.index(msg.content[6:])].removecard(ctx)
                                        if (aliveplayers == 1):
                                            gamestate = "notrunning"
                                            break
                                        break
                                    else:
                                        await ctx.send(f"You can't coup {msg.content[6:]} because he is dead!")
                                else:
                                    await ctx.send(f"\"{msg.content[6:]}\" is not a player! Valid players are {listarray(playernames)}.")
                            else:
                                await ctx.send("You don't have enough coins to use coup!")
                        else:
                            await ctx.send("You can't coup yourself!")
                    else:
                        await ctx.send("You need to specify a target! Usage: !coup <playername>")
        turn += 1
        currentplayer += 1
        if (currentplayer == len(players)):
            currentplayer = 0
        while (not players[currentplayer].isalive):
            currentplayer += 1
            if (currentplayer == len(players)):
                currentplayer = 0
    if (turn > 1):
        await ctx.send(f"{players[currentplayer].name} wins after {turn} turns! Thanks for playing!")
    else:
        await ctx.send(f"{players[currentplayer].name} wins after 1 turn! Thanks for playing!")
    await ctx.send("Use !coupgame to start another game!")
    random.shuffle(secret)
    await players[currentplayer].context.author.send(f"This is a reward for your victory. Don't tell anyone! Here is your rare link: {random.choice(secret)}")
    reset()



@client.event #ignores command not found errors
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@client.event
async def on_ready():
    print("Bot is ready.")

@client.command()
async def ping(ctx):
    await ctx.send(f"Your ping is {round(client.latency*1000)}ms")

@client.command()
async def coupgame(ctx):
    global gamestate
    global startingcontext
    if (gamestate == "notrunning"):
        if (not ctx.channel.type is discord.ChannelType.private):
            await ctx.send("Let\'s play coup! Say !join to join and !start to start")
            gamestate = "accepting players"
            startingcontext = ctx
            print ("Accepting players...")
        else:
            await ctx.send("You can only start the game in the coup server!")
    else:
        await ctx.send("Game already running!")

@client.command()
async def start(ctx):
    if (gamestate == "accepting players" and len(players) < 2):
        await ctx.send("Not enough players to start!")
    elif (gamestate == "accepting players"):
        if (startingcontext.author == ctx.author):
            if (startingcontext.channel == ctx.channel):
                await game(startingcontext)
            else:
                await ctx.send("You can only start the game in the coup server!")
        else:
            await ctx.send("Only the person who said !coupgame can start the game!")

@client.command()
async def join(ctx):
    global aliveplayers
    if (gamestate == "accepting players"):
        if (not ctx.author.name in playernames):
            if (ctx.channel == startingcontext.channel):
                await ctx.send(f"{ctx.author.name} is playing!")
                print (f"{ctx.author.name} is playing")
                aliveplayers += 1
                players.append(player(ctx))
                playernames.append(str(ctx.author.name))
                if (len(players) == 6):
                    await game(startingcontext)
            else:
                await ctx.send("You can only join the game in the coup server!")
        else:
            await ctx.send(f"{ctx.author.name}, you are already playing!")
    elif (gamestate == "notrunning"):
        await ctx.send("Cannot join because game isnt running! Say !coupgame to start")

client.run(API_KEY)
