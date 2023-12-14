import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM, Flatten, Dropout


deck = []
colors =["Red", "Green", "Blue", "Yellow"]
action = ["Reverse", "Skip", "PlusTwo"]
num_decks = 4
num_players = 3

def createDeck(num_decks):
    for i in range(num_decks):
    #Put number cards into deck
        for i in range(4):
            numbers = 0
            for j in range(10):
                card = colors[i] + '_' + str(j)
                #there is only 1 zero for each color so only add one 0
                if numbers == 0:
                    deck.append(card)
                #Two cards for each color so add two times
                else:
                    deck.append(card)
                    deck.append(card)
                numbers += 1
        #This is for the plus 2, reverse, and skip
        for i in range(4):
            index = 0 
            for j in range(3):
                card = colors[i] + '_' + action[index]
                deck.append(card)
                deck.append(card)
        #wild cards, may not use these though in final product
        for i in range(4):
            deck.append("Wild_Four")
        for i in range(8):
            deck.append("Wild_Wild")
    #shoe = random.shuffle(deck)
    
    return deck
#the random.shuffle() wasnt mixing the cards well enough
#so made a function to shuffle the deck better
#also to later on shuffle the center card to maybe have a second place option
def shuffleIt(deck):
    for pos in range(len(deck)):
        #there are 108 in the standard deck, we are using 2 so its 216 - 1
        randPos = random.randint(0, 215)
        deck[pos], deck[randPos] = deck[randPos], deck[pos]
    return deck


#Draws cards for players
def drawCards(num_cards):
    cards = []
    for i in range(num_cards):
        cards.append(shoe.pop(0))
    
    new_hand = []
    spltCard = ''
    for card in cards:
        if card == 'Wild':
            spltCard == 'Wild_Wild'
        elif card == 'WildFour':
            spltCard == 'Wild_Four'
        else:
            spltCard = card.split('_')
        new_hand.append(spltCard)
    return new_hand

   



center_card_count = 0 
reverseDirection = 1
color_dict = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}

#This is where the magic happens with what to play based on color and value

def play_UNO(center_card, player_hands, curr_player_results):
    
    what_played = []
    cardPickUp = 0
    cardsPlayed = 0
    
    for player in range(num_players):
        
        #split the center card into color and val for comparisons
        #center_color, center_val = center_card[-1]
        #check through each card to compare to the center card
        for player in player_hands:
            index = 0
            if (len(player)) > 0:
                for card in player:
                    for mid in center_card:
                        #if the center card has a plus two or plus four, add those cards to hand
                        if mid[1] == 'PlusTwo':
                            player = player + drawCards(2)
                            cardPickUp += 2
                        elif mid[1] == 'Four':
                            player = player + drawCards(4)
                            cardPickUp += 4
                        #Compare the cards and find out if you can play or if you have to draw
                        if mid[0] == 'Wild':
                            center_card.append(player[card].pop(0))
                            cardsPlayed += 1
                            what_played = what_played + player
                        #for now this will also play skips and reverses with no heppening
                        #first color
                        elif (mid[0] == 'Red') and (card[0] == 'Red'):
                            center_card.append(player[card].pop(0))
                            cardsPlayed += 1
                            what_played= what_played + player
                            color_dict['Red'] += 1
                        elif (mid[0]== 'Green') and (player[0] == 'Green'):
                            color_dict['Green'] += 1
                            center_card.append(player[card].pop(0))
                            cardsPlayed += 1
                            what_played= what_played + player
                        elif (mid[0]== 'Blue') :
                            color_dict['Blue'] += 1
                            center_card.append(player[card].pop(0))
                            cardsPlayed += 1
                            what_played= what_played + player
                        elif (mid[0]== 'Yellow') and (player[0] == 'Yellow'):
                            color_dict['Yellow'] += 1
                            center_card.append(player[card].pop(0))
                            cardsPlayed += 1
                            what_played= what_played + player
                        #Then value
                        elif (mid[1] == card[1]):
                            center_card.append(player[card].pop(0))
                            
                            cardsPlayed += 1
                            what_played= what_played + player
                        #If not value then we play any regular wild we have
                        elif (card[0] == 'Wild' and card[1] == "Wild"):
                            center_card.append(player[card].pop(0))
                            cardsPlayed += 1
                            what_played= what_played + player
                        #And if all else fails and we have no other card to play but the plus four
                        #we play the plus four. There is not change in color 
                        elif(card[0] == 'Wild') and (card[1] == 'Four'):
                            center_card.append(player[card].pop(0))
                            cardsPlayed += 1
                            what_played= what_played + player

                        else:
                            player = player + drawCards(1)
                            cardPickUp += 1
                        print(player)
                        print(' ')

                index += 1
            else:
                print("A player has won, Game over, Starting next")
    return cardPickUp, cardsPlayed, color_dict, what_played


simulations = 5

center_card_history = []
player_card_history = []
card_PickUp_history = []
player_live_total = []


first_game = True
prev_sim = 0
sim_number_list = []
new_sim = []
games_played_in_sim = []
center_card = []

for sim in range(simulations):
    games_played = 0

    s = createDeck(num_decks)
    sh = shuffleIt(s)
    sho = shuffleIt(sh)
    shoe = shuffleIt(sho)

    while(len(shoe) > 5):
        curr_player_results = np.zeros((1, num_players))
        player_hands = [ [] for player in range(num_players)]

        for player, hand in enumerate(player_hands):
            player_hands[player] = drawCards(7)
        

        #create the center card used to play
        center_card = drawCards(1)
        

        cardPickUp, cardsPlayed, color_dict, what_played  = play_UNO(center_card, player_hands, curr_player_results)

        #Center card history
        center_card_history.append(center_card)
        card_PickUp_history.append(cardPickUp)
        player_card_history.append(what_played)

        red = color_dict['Red']
        green = color_dict['Green']
        blue = color_dict['Blue']
        yellow = color_dict['Yellow']

        if sim != prev_sim:
            new_sim.append(1)
        else:
            new_sim.append(0)

        if first_game == True:
            first_game = False
        else: 
            games_played += 1
        sim_number_list.append(sim)
        games_played_in_sim.append(games_played)
        prev_sim = sim


        #Make a dataframe to display information 
        model_df = pd.DataFrame()
        model_df['center_card'] = center_card_history
        model_df['cards_pickUp'] = card_PickUp_history
        model_df['what_played'] = player_card_history
        model_df['total_red'] = red
        model_df['total_green'] = green
        model_df['total_blue'] = blue
        model_df['total_yellow'] = yellow
        model_df.to_csv('UNOsim.csv')
        print(model_df.info())
        print(model_df.describe())
