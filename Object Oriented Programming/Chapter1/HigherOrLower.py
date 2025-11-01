import random

SUIT_TUPLE = ('Spade', 'Hearts', 'Clubs', 'Diamonds')
RANK_TUPLE = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')

NCARDS=8

# pass deck to this function and pick one card form the deck 
def getCard(deckListIn):
    thisCard = deckListIn.pop()
    return thisCard

# pass deck to shuffle the card 
def shuffle(deckListIn):
    deckListOut = deckListIn.copy()
    random.shuffle(deckListOut)

    return deckListOut

# Main Card 
print("Welcome to Higher or Lower")
print("You have to choose whether the next card to be shown will be higher or lower")
print("Getting the card right will award you 20 points; get it wrong you lose 15 points")
print("You have 50 points to start with")
print()

# create the deck 
startingDeckList=[] 
for suit in SUIT_TUPLE:
    for thisValue, rank in enumerate(RANK_TUPLE):
        cardDict = {'rank': rank, 'suit': suit, 'value': thisValue + 1}
        startingDeckList.append(cardDict)

score=50 

# print(startingDeckList)

while True:
    print()
    gameDeckList = shuffle(startingDeckList)
    currentCardDict = getCard(gameDeckList)

    currentCardRank = currentCardDict['rank']
    currentCardSuit = currentCardDict['suit']
    currentCardValue = currentCardDict['value']

    print('Starting card is: ', currentCardRank, 'of', currentCardSuit)
    print()

    for cardNumber in range(0, NCARDS):
        answer = input('Will next card be higher or lower than ' + currentCardRank + ' of ' + currentCardSuit + '?    (enter h or l): ')
        
        # force answer to be in lowercase 
        answer = answer.casefold()

        nextCardDict = getCard(gameDeckList)

        nextCardRank = nextCardDict['rank']
        nextCardSuit = nextCardDict['suit']
        nextCardValue = nextCardDict['value']        

        print('Next card is: ', nextCardRank, 'of', nextCardSuit)

        if answer == 'h':
            if nextCardValue > currentCardValue:
                print('You got it right.. It was higher')
                score = score + 20 

            else: 
                print('Sorry it was not higher')
                score = score - 15

        elif answer == 'l': 
            if nextCardValue < currentCardValue:
                print('You got it right.. It was lower')
                score = score + 20 

            else: 
                print('Sorry it was not lower')
                score = score - 15            
        print ('Your score is ', score)
        print ()

        currentCardRank = nextCardRank
        currentCardValue = nextCardValue 

    goAgain = input("Want to play again press ENTER else type q to quit:   ")

    if goAgain == 'q':
        break

print ('BYE')