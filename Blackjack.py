'''
Made By: Sean Stach
Last Edited: 17/03/2018

This is a game of Black jack that only supports up to one player and has nearly
all functionality of a normal blackjack game. The game differs from casino to
casino so the rules may not be the same as you expect.

You can find the specific rules for this blackjack under the rules function or
by pressing r in the console.

It was progammed with out much use of Object Orientation which I accustomed to.

'''

import random

'''

    FUNCTIONS
    
'''

#Builds a deck of cards and shuffles
#Playing with two decks as one deck isn't common unless odds are changed
#Return: (list) shuffled deck
def shuffleDeck():
    deck = []
    for suit in SUITS:
        for card in CARDS:
            deck.append([(suit, card), False])
            deck.append([(suit, card), False])
    random.shuffle(deck)
    print("\n~ Deck shuffled! ~")
    return deck

#Draws a card to a hand
#Par1: (list) deck to draw from
#Par2: (list) hand to draw to
#Par3: (str) Name of hand owner
#Par4: (bool) draw card face down
#Par5: (num) hand number to print
def drawCard(deck, hand, name, faceDown=False, handNumber=0):
    hand.append(deck.pop(len(deck)-1))
    if(faceDown):
        hand[len(hand)-1][1] = True
    if(handNumber == 0):
        print("\n~ " + name + " receives " + cardName(hand[len(hand)-1]) + " ~")
    else:
        print("\n~ " + name + " receives " + cardName(hand[len(hand)-1]) + 
              " in Hand " + str(handNumber) + "~")
    
    return None

#Reveals dealer hole card
#Par1: (list) dealer hand
def dealerReveal(dealerHand):
    if(dealerHand[0][1] == False):
        return None
    
    dealerHand[0][1] = False
    print("\n~ Dealer revealed: " + cardName(dealerHand[0]) + " ~")
    
    return None

#Makes a card name
#Par1: (tuple) card tuple
#Return: (str) card string
def cardName(card):
    if(card[1] == True):
        return "Face Down Card"
    else:
        return "%s %s" % (card[0][0], card[0][1])

#Prints out the given hand
#Par1: (llist) Hand to print
#Par2: (str) name of hand owner
#Par3: (num) number of hand to print
def printHand(hand, name, handNumber=0):  
    if(handNumber==0):
        print("\n" + name + " Hand:")
    else:
        print("\n" + name + " Hand " + str(handNumber) +":")
    for card in hand: 
        print("- ", cardName(card))
    
    isFirstCardFaceDown = hand[0][1]    
    if(isFirstCardFaceDown):
        print("Est. Total: " + str(handValue(hand, True)) + " + 1-11")
    else:
        print("Total: " + str(handValue(hand)))
        
    return None
      
#Returns the value of hand, returns value without hidden card if set to hidden
#Par1: (list) Hand to evaluate
#Par2: (bool) Add Facedown card valuie
#Return: (int) value of hand
def handValue(hand, hidden=False):
    handValue = 0
    aces = 0
    for card in hand:
        cardName = card[0][1]
        if(hidden):
            hidden = False
            continue
        if(cardName == "Ace"):
            aces+=1;
            continue
        value = 0
        if(cardName == "King" or cardName == "Queen" or 
           cardName == "Jack"):
            value = 10
        else:
            value = int(cardName)
        handValue += value
    
    while (aces != 0):
        if(handValue + 11 <= 21):
            handValue += 11
        else:
            handValue += 1
        
        aces -= 1
            
    return handValue;    

#Work out the payout for the player
#Par1: (list) hand of dealer
#Par2: (list hand of player
def payOut(dealerHand, playerHands, index, bettingAmount):  
    
    playerHand = playerHands[index]
    dealerValue = handValue(dealerHand)
    playerValue = handValue(playerHand)
    dealerBlackjack = len(dealerHand) == 2 and dealerValue == 21
    playerBlackjack = len(playerHand) == 2 and playerValue == 21 and len(playerHands) == 1
    
    amount = 0
    if(dealerBlackjack and not playerBlackjack):
        print("\nDealer blackjack!")
        amount = -bettingAmount
    elif(playerBlackjack and not dealerBlackjack):
        print("\nBlackjack Win!")
        amount = bettingAmount * 1.50
    elif((playerValue > dealerValue or dealerValue > 21) and 
         playerValue <= 21):
        print("\nWin!")
        amount = bettingAmount
    elif(playerValue == dealerValue and playerValue <= 21):
        print("\nDraw!")
    else:
        print("\nLost!")
        amount = -bettingAmount   
    return amount

#Alters amount of cash
#Par1: (int) The amount to alter
def alterCash(amount):
    if(amount < 0):
        print("\n-- Lost $" + str(abs(amount)) + " --")
    elif(amount > 0):
        print("\n++ Gained $" + str(abs(amount)) + " ++")
    
    return amount

#Asks a user for an amount to bet with
#Parameter 1: (string) Text to display to the user
#Parameter 2: (int) limit of bet
#Paramater 3: (int) what intervals that bet can be taken as
#Return: (int) the amount the user bet with
def betInput(toDisplay, limit, interval):
    while(True):
        print(toDisplay)
        bet = input()
        
        if(not bet.isdigit()):
            print("\nMust only enter whole numbers!")
            continue
    
        bet = int(bet)
    
        if(bet % interval != 0):
            print("\nMust be in intervals of %d!" % interval)
            continue
    
        if(bet > limit):
            print("\nMust not be over %d!" % limit) 
            continue
        
        return bet
    return None

#Prints rules specific to this blackjack
def printRules():
    print("\nRules:")
    print("- Uses two decks.")
    print("- Dealer doesn't draw on soft 17.")
    print("- Insurance:")
    print("-- Can do insurance wager between 0 and original betting amount.")
    print("-- If you bet maximum insurance with blackjack you'll receive 2x")
    print("-- your original bet and end your hand.")
    print("- Surrender:")
    print("-- Can surrender only after drawing first two cards.")
    print("-- Will get 50% of money back.")
    print("- Split:")
    print("-- Can split a maximum of 3 times.")
    print("-- Can not get blackjack on a split.")
    print("-- No special rules for splitting on ace.")
    print("- Double:")
    print("-- Double your bet and only receive one extra card.")
    print("-- May only be exactly double of current bet.")

#Setup the game
#Par1: (list) used deck
#Par2: (list) player hands
#Par3: (list) dealer hand
#Return: (int) betting amount
def gameSetup(deck, hands, dealer):
    
    #Player starting hand
    hands.append([])
    drawCard(deck, hands[0], "Player")
    drawCard(deck, hands[0], "Player")
    
    if(handValue(hands[0]) == 21):
        print("\nBlack jack!")
    
    #Dealer hand
    drawCard(deck, dealer, "Dealer", True)
    drawCard(deck, dealer, "Dealer")
    
    return bettingAmount
  
#Double bet
#Par1: (int) bet amount
#Par2: (int) hand index
#Return: (int) bet amount
def double(bet, idx):
    print("\nDouble down!")
    doubled[idx] = True
    return bet

#Add a card to hand
#Par1: (list) deck to add to
#Par2: (list) player hands
#Par3: (int) current player hand index
#Return: (int) next hand index
def hit(deck, hands, index): 
    if(len(hands) == 1):
        drawCard(deck, hands[index], "Player")
    else:
        drawCard(deck, hands[index], "Player", False, index+1)
    
    #Check for bust
    if(bustCheck(hands[index], "Player", index+1)):
        return index+1
    return index


#Splits the hand into two
#Par1: (list) deck to get cards from
#Par2: (list) players hands
#Par3: (int) index of current hand
def split(deck, hands, handIdx):    
    print("\nSplit hand!")
    hands.append([hands[handIdx].pop(1)])
    drawCard(deck, hands[handIdx], "Player", False, handIdx+1)
    drawCard(deck, hands[len(hands)-1], "Player", False, len(hands))
    return None

#Checks to see if can split hand
#Par1: (list) hands to check
#Par2: (str) index of hand
#Return: (bool) if can split
def canSplit(hands, index):
    hand = hands[index]
    firstCardName = hand[0][0][1]
    secondCardName = hand[1][0][1]
    if(len(hand) !=2):
        return False
    if(len(hands) < 4 and (hand[0][0][1] == hand[1][0][1] or 
       ((firstCardName == "King" or firstCardName == "10" or
        firstCardName == "Queen" or firstCardName == "Jack") and
        (secondCardName == "King" or secondCardName == "10" or
         secondCardName == "Queen" or secondCardName == "Jack")))):
           return True
    return False
           
#Checks to see if hand is bust
#Par1: (list) hand to check
#Par2: (str) name of hand owner
#Par3: (num) hand number
#Return: (bool) if bust
def bustCheck(hand, name, number=0):
    if(handValue(hand) > 21):
        if(number==0):
            print("\n" + name + " bust!")
        else:
            print("\n%s Hand %d bust!" % (name, number))
        return True
    return False            

'''

    VARIABLES
    
'''
    
#Tuples for card generation
SUITS = ("♠", "♦", "♣", "♥")   
CARDS = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", 
         "Queen", "King")     
#List of all actions
ACTIONS = {'p':"S(p)lit", 'u':"S(u)rrender", 'l':"(L)eave", 's':"(S)tand"
           , 'a':"(A)lter bet", 'h':"(H)it", 'b':"(B)et", 'd':"(D)ouble",
           't':"Player S(t)atistics", 'r':"House (R)ules"} 

#Game state variables
deck = []
cash = 1000
bettingAmount = 0
insuranceAmount = 0
playerHands = []
dealerHand = []
currentHandIdx = 0
doubled = {} #Key is hand index and value is if hand should be doubled

#Stats
handsPlayedStat = 0
standStat = 0
evenMoneyStat = 0
splitStat = 0
doubleStat = 0
bustStat = 0
hitStat = 0
surrenderStat = 0
insuranceStat = 0
blackJackStat = 0
drawStat= 0
insuranceAmtStat = [] #Record of amounts spent on insurance
betAmtStat = [] #Record of amounts spent on initial bet
winTotal = [] #Record of individual accounts of money earned
loseTotal = [] #Record of individual accounts of money lost


'''

    THE GAME LOOP

'''

userInput = ""
print("\nWelcome to Digital Casino!")

while(cash > 0 and userInput != 'l'):    
    #Check available actions taking from action var
    currentActions = []
    
    #Starting actions
    if(len(playerHands) == 0):
        currentActions.append('b')
        if(bettingAmount <= cash and bettingAmount > 0):
            currentActions.append('a')   
        currentActions.append('r')
        currentActions.append('t')
        currentActions.append('l')
    #Playing actions
    elif(currentHandIdx < len(playerHands) and 
       handValue(playerHands[currentHandIdx]) < 21 and
       handValue(dealerHand) < 21):
        currentActions.append('h')
        currentActions.append('s')
        if(bettingAmount*2 <= cash):
            currentActions.append('d')
        if(cash-bettingAmount*(len(playerHands)+1) and 
           canSplit(playerHands, currentHandIdx)):
            currentActions.append('p')
        if(len(playerHands) == 1 and len(playerHands[0]) == 2):
            currentActions.append('u')  
    
    if(len(playerHands) != 0 and currentHandIdx < len(playerHands) and
       handValue(playerHands[currentHandIdx]) == 21):
        currentHandIdx+=1
        continue
    
    #Handle user input
    userInput = ""
    
    while(not userInput in currentActions and len(currentActions) > 0):
        
        #Print game state
        if(len(playerHands) > 0):
            printHand(dealerHand, "Dealer")
            printHand(playerHands[currentHandIdx], "Player", currentHandIdx+1)
        
        print("\nCurrent Balance: $" + str(cash))
        if(bettingAmount > 0 and bettingAmount <= cash):
            print("Current Bet: $%d" % bettingAmount)
        for action in currentActions:
            print(ACTIONS[action])
    
        print("\nChoose an action:")
        userInput = input().lower()
    
    if(userInput=='r'):
        printRules()
        continue
    
    if(userInput=='t'):
        print("\nPLAYER STATISTICS:")
        print("Hands Played: %d Hits: %d" % (handsPlayedStat, hitStat))
        print("Stands : %d Splits: %d" % (standStat, splitStat))
        print("Doubles: %d Surrenders: %d" % (doubleStat, surrenderStat))
        print("Busts: %d Blackjacks: %d" % (bustStat, blackJackStat))
        print("Total Winnings: %d Total Losses: %d Times Made Even: %d" % 
              (sum(winTotal), sum(loseTotal), drawStat))
        if(len(winTotal) > 0):
            print("Avg Winnings: %d" % 
                  (sum(winTotal)/len(winTotal)))
        if(len(loseTotal) > 0):
            print("Avg Losings: %d" % 
                  (sum(loseTotal)/len(loseTotal)))
        if(len(loseTotal) > 0 and len(winTotal) > 0):
            print("Earnings Per Hand: %d" % 
                  ((sum(winTotal)-sum(loseTotal))/handsPlayedStat))
        if(len(betAmtStat) > 0):
            print("Avg Bet Amount: %d" % (sum(betAmtStat)/len(betAmtStat)))
        if(len(insuranceAmtStat) > 0):
            print("Avg Insurance Amount: %d" % 
                  (sum(insuranceAmtStat)/len(insuranceAmtStat)))
        continue
    
    if(userInput=='b' or userInput=='a'):
        if(bettingAmount == 0 or bettingAmount > cash or userInput=='a'):
            bettingAmount = betInput("\nInput an interval of 2 as bet:", 
                                     cash, 2)
        
        betAmtStat.append(bettingAmount)
        deck = shuffleDeck()
        dealerHand = []
        currentBet = bettingAmount
        gameSetup(deck, playerHands, dealerHand)
        handsPlayedStat+=1
        if(handValue(playerHands[0]) == 21):
            blackJackStat+=1
        currentHandIdx = 0
        doubled = {}
        #Insurance check
        dealer2ndCard = dealerHand[1][0][1]
        if(dealer2ndCard == "Ace"):
            insuranceAmount = betInput("\nPlease enter desired insurance amount:", 
                                       bettingAmount/2, 1)
            insuranceAmtStat.append(insuranceAmount)
            
            if(insuranceAmount > 0):
                insuranceStat+=1
            #Take even money            
            if(handValue(playerHands[0]) == 21 and 
               insuranceAmount == bettingAmount/2):
                cash+= alterCash(bettingAmount)
                
                winTotal.append(bettingAmount)
                insuranceAmount = 0
                evenMoneyStat+=1
        
        if(dealer2ndCard == "Ace" or dealer2ndCard == 10 or
           dealer2ndCard == "Jack" or dealer2ndCard == "Queen" or
           dealer2ndCard == "King"):    
            print("\n~ Dealer peeks at face down card ~")
        if(handValue(dealerHand) != 21 and insuranceAmount > 0):
            print("\nLost insurance!")
            cash+=alterCash(-insuranceAmount)
            loseTotal.append(insuranceAmount)
            insuranceAmount = 0
        continue
    
    if(userInput == 'l'):
        continue
    
    if(userInput=='s'):
        standStat+=1
        currentHandIdx+=1
        continue
    
    if(userInput=='d'):
        doubleStat+=1
        bettingAmount = double(bettingAmount, currentHandIdx)
        hit(deck, playerHands, currentHandIdx)
        currentHandIdx+=1
        continue
    
    if(userInput=='h'):
        hitStat+=1
        print("\nHit!")
        currentHandIdx = hit(deck, playerHands, currentHandIdx)
        continue
    
    if(userInput=='p'):
        splitStat+=1
        split(deck, playerHands, currentHandIdx)
        continue
    
    if(userInput=='u'):
        print("\nSurrendered!")
        cash+=alterCash(int(-bettingAmount/2))
        loseTotal.append(bettingAmount/2)
        surrenderStat+=1
        playerHands = []
        
    dealerReveal(dealerHand)
    
    #Dealer card draw, no soft 17
    while(handValue(dealerHand) < 17):
        drawCard(deck, dealerHand, "Dealer")
    
    #Dealer bust
    bustCheck(dealerHand, "Dealer")  
    
    #Handle final payouts
    printHand(dealerHand, "Dealer") 
    
    #Record busts
    for hand in playerHands:
        if(handValue(hand) > 21):
            bustStat+=1
    
    #Resolve hands
    if(len(playerHands) == 1):
        printHand(playerHands[0], "Player")
        if(0 in doubled and doubled[0] == True):
            currentBet = bettingAmount * 2
        else:
            currentBet = bettingAmount
        cashWon = payOut(dealerHand, playerHands, 0, currentBet)
            #Resolve insurance
            
        cashChange = 0
        if(insuranceAmount != 0 and handValue(dealerHand) == 21):
            print("\nWon insurance!")
            cashChange = alterCash(insuranceAmount)
            insuranceAmount = 0
        
        cashChange = alterCash(cashWon)
        
        cash+=cashChange
        if(cashChange < 0):
            loseTotal.append(-cashChange)
        elif(cashChange > 0):
            winTotal.append(cashChange)
        else:
            drawStat+=1
    else:
        for i in range(len(playerHands)): 
            if(i in doubled and doubled[i] == True):
                currentBet = bettingAmount * 2
            else:
                currentBet = bettingAmount
            printHand(playerHands[i], "Player", i+1) 
            cashChange = alterCash(payOut(dealerHand, playerHands, i, currentBet))
            cash+=cashChange
            if(cashChange < 0):
                loseTotal.append(-cashChange)
            elif(cashChange > 0):
                winTotal.append(cashChange)
            else:
                drawStat+=1
    playerHands = []
if(cash == 0):
    print("\nYou're out of money! Get out of the casino!")
else:
    print("\nYou've left with $" + str(cash) + 
          ". Please visit our establishment again!")
    