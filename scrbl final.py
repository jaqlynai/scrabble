'''
CS30 Final Project
Carson + Jaqlyn
April 13 2022
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
import scrbl #module of extra scrabble functions

t_word = [[0, 0], [0, 7], [0, 14], [7, 0], [7, 14], [14, 0], [14, 7], [14, 14]] #triple word tiles
d_letter = [[0, 3], [0, 11], [2, 6], [2, 8], [3, 0], [3, 7], [3, 14], [6, 2], [6, 6], [6, 8], [6, 12],
            [7, 3], [7, 11], [8, 2], [8, 6], [8, 8], [8, 12], [11, 0], [11, 7], [11, 14], [12, 6],
            [12, 8], [14, 3], [14, 11]] #double letter tiles

#************************* start class LetterTile *********************************

class LetterTile(object):
    ''' Represents a letter tile

    Attributes:
        Letter (str)
        Letter Amount (int) (amount of each letter in a typical Scrabble game)
        Letter Score (int) (how much each letter scores)

    ex: 'A', 9, 1
    '''
    
    def __init__(self, letter = '', amount = 0, score = 0):
        self.letter = letter
        self.amount = amount
        self.score = score
    
#**************************** end class LetterTile *********************************

class DrawPile():
    
    def __init__(self):
        self.letterlist = [] #stores list of letter strings
        self.Tilelist = [] #stores list of LetterTile() objects

        mynewhandle = open("Letters.csv", "r")
        
        theline = mynewhandle.readline() #skip first line with column headings
        somedata = LetterTile() #create a LetterTile object
        self.letterlist.append(somedata)
        
        count = 0 #to count how many sets of data are read
        
        while True:
            theline = mynewhandle.readline()

            count += 1
            
            if len(theline) == 0:
                break
            
            else:
                alist = theline.split(",")
                        
                somedata = LetterTile(str(alist[0]), int(alist[1]), int(alist[2]))
                self.Tilelist.append(somedata)
                
                #adds the proper amount of letters to letterlist
                #ex. adds letter 'A' 9 times
                for i in range(int(alist[1])):
                    self.letterlist.append(alist[0])
        
        self.letterlist.remove(self.letterlist[0]) #removes blank/header data
        
        mynewhandle.close()

        self.numData = count
        
    def draw_tile(self): #returns a randomly drawn letter value
        letter = random.choice(self.letterlist)
        self.letterlist.remove(letter)
        return letter

    def score(self, letter): #returns the score attribute of a letter
        for i in range(self.numData):
            if self.Tilelist[i].letter == letter:
                return self.Tilelist[i].score

#****************************************** end of class DrawPile **************************************

class playerHands(DrawPile):
    '''Represents the series of letters a player has

    Has a parent class of DrawPile

    Attributes:
        name (str) (represents the player name)
    '''
    
    def __init__(self, name = ''):
        DrawPile.__init__(self) #initializes DrawPile functions
        
        self.name = name #ex. 'P1'
        self.p_hand = [] #represents list of tiles in player's hand
             
        for i in range(7): #draws 7 random tiles into player's hand
            draw = super().draw_tile() #draw_tile() function from parent class
            self.p_hand.append(draw)    
        
    def draw_random(self): #appends randomly drawn tile to player's hand
        draw = super().draw_tile()
        self.p_hand.append(draw)

    def word_score(self, word, direction, place_point, points): #returns score of a word
        x = place_point[0]
        y = place_point[1]

        coord_list = []

        point = 0

        if direction == 'right':
            for i in range(len(word)):
                coord = (x + i, y) #runs through each coordinate in word
                if coord in d_letter: #letter score multiplied by 2 on double letter tiles
                    point += super().score(word[i]) * 2
                else:
                    point += super().score(word[i])
                coord_list.append(coord)
        else:
            for i in range(len(word)):
                coord = (x, y + i)
                if coord in d_letter:
                    point += super().score(word[i]) * 2
                else:
                    point += super().score(word[i])
                coord_list.append(coord)
        
        for coord in coord_list:
            if coord in t_word: #overall word score multiplied by 3 on triple word tiles
                point = point * 3
        
        points += point

        return points

#*********************************** end of class playerHands ****************************************

#initialize both playerHands objects
p1 = playerHands("P1")
p2 = playerHands("P2")

p1_score = 0
p2_score = 0

turn = 0

print("Welcome to Jaqlyn and Carson's Scrabble Game!\n")
rules = input("Would you like to see the rules before playing? (Y/N)\n")
if rules == "Y" or rules == "y":
    read_rules = open("Rules.txt", "r") #txt file of rules
    print() #white space
    for line in read_rules:
        print(line, end = "")
    print("\n")

while True:
    if turn % 2 == 0: #player one
        while True:
            print(p1.name + ' score: ' + str(p1_score)) #prints player one's score

            print(p1.name + ' tiles:', end = ' ') #prints player one's tiles
            print(p1.p_hand)
            
            user_word = input('Enter your word: ').upper()

            if type(user_word) != str:
                print("Invalid word.")
                continue

            if '?' in p1.p_hand: #checks if user wants to use blank tile
                blank = input('Are you using your blank tile? (Y/N): ')
                if blank == 'Y' or blank == 'y':
                    temp = input('Enter blank tile letter: ').upper()
                    indx = p1.p_hand.index('?')
                    p1.p_hand[indx] = temp #sets '?' to desired letter value

            user_x = input('Enter x-coordinate: ')
            user_y = input('Enter y-coordinate: ')
            user_dir = input('"right" or "down": ')
            
            #checks and converts coordinates to int
            if user_x.isdigit():
                user_x = int(user_x)
            else:
                print("Invalid x value.")
                continue
            
            if user_y.isdigit():
                user_y = int(user_y)
            else:
                print("Invalid y value.")
                continue
            
            #checking for valid inputs
            if user_x > 14 or user_x < 0: #checks bounds
                print("Invalid x value.")
                continue
            if user_y > 14 or user_y < 0:
                print("Invalid y value.")
                continue
            if user_dir != "right" and user_dir != "down":
                print("Invalid direction.")
                continue
            
            user_start = (user_x, user_y)
            
            check_borders = scrbl.check_borders(user_word, user_dir, user_start)
            
            if check_borders == False:
                print("Your word is not playable. Try again.")
                continue
            
            if turn == 0:
                temp = scrbl.play_first(user_word, user_dir, user_start, p1.p_hand) 
            
            else:
                temp = scrbl.place_word(user_word, user_dir, user_start, p1.p_hand)

            if temp == False:
                print('Your word is not playable. Try again.')
                continue
            else:
                p1_hand = temp
                p1_score += p1.word_score(user_word, user_dir, user_start, p1_score)
                
            while len(p1.p_hand) != 7:
                p1.draw_random()
            
            p2.letterlist = p1.letterlist #updates draw pile for player two
            break
            
    else: #player two
        while True:
            print(p2.name + ' score: ' + str(p2_score)) #prints player two's score

            print(p2.name + ' tiles:', end = ' ') #prints player two's tiles
            print(p2.p_hand)
            user_word = input('Enter your word: ').upper()
            if type(user_word) != str:
                print("Invalid word.")
                continue

            if '?' in p2.p_hand: #checks if user wants to use blank tile
                blank = input('Are you using your blank tile? (Y/N): ')
                if blank == 'Y' or blank == 'y':
                    temp = input('Enter blank tile letter: ').upper()
                    indx = p2.p_hand.index('?')
                    p2.p_hand[indx] = temp #sets '?' to desired letter value

            user_x = input('Enter x-coordinate: ')
            user_y = input('Enter y-coordinate: ')
            user_dir = input('"right" or "down": ')
            
            #checks and converts coordinates to int
            if user_x.isdigit():
                user_x = int(user_x)
            else:
                print("Invalid x value.")
                continue
            
            if user_y.isdigit():
                user_y = int(user_y)
            else:
                print("Invalid y value.")
                continue
            
            #checking for valid inputs
            if user_x > 14 or user_x < 0: #checks bounds
                print("Invalid x value.")
                continue
            if user_y > 14 or user_y < 0:
                print("Invalid y value.")
                continue
            if user_dir != "right" and user_dir != "down":
                print("Invalid direction.")
                continue

            user_start = (user_x, user_y)
            
            check_borders = scrbl.check_borders(user_word, user_dir, user_start)
            check_spelling = scrbl.check_spelling(user_word, p2.p_hand)
            
            if check_spelling == False:
                continue
            
            if check_borders == False:
                print('Your word is not playable. Try again.')
                continue
            
            temp = scrbl.place_word(user_word, user_dir, user_start, p2.p_hand)

            if temp == False:
                print('Your word is not playable. Try again.')
                continue
            else:
                p2.p_hand = temp
                p2_score += p2.word_score(user_word, user_dir, user_start, p2_score)
                
            print(p2.letterlist)
            while len(p2.p_hand) != 7:
                p2.draw_random()
                
            p1.letterlist = p2.letterlist #updates draw pile for player one
            
            break

    turn += 1
    if (turn + 2) % 2 == 0:
        scrbl.plot_points(p1_score, p2_score, int(turn/2)) #graphs results after one round