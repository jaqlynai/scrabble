#Scrabble Functions

import enchant
# dict = enchant.Dict("en_US")
import colorama
from colorama import init, Fore, Style
init()
import matplotlib.pyplot as plt

t_word = [[0, 0], [0, 7], [0, 14], [7, 0], [7, 14], [14, 0], [14, 7], [14, 14]] #triple word tiles
d_letter = [[0, 3], [0, 11], [2, 6], [2, 8], [3, 0], [3, 7], [3, 14], [6, 2], [6, 6], [6, 8], [6, 12],
            [7, 3], [7, 11], [8, 2], [8, 6], [8, 8], [8, 12], [11, 0], [11, 7], [11, 14], [12, 6],
            [12, 8], [14, 3], [14, 11]] #double letter tiles

#board represents tiles; zeroes as placeholders
board = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]

#******************************* functions *************************************

def draw_board():

    for row in range(15):
        for col in range(15):
            square = '□' #board tiles
            
            if [row, col] in t_word: #sets triple word tiles as blue
                square = Fore.CYAN + Style.BRIGHT + square + Style.RESET_ALL

            elif [row, col] in d_letter: #sets double letter tiles as red
                square = Fore.RED + Style.BRIGHT + square + Style.RESET_ALL
        
            if board[row][col] == square or board[row][col] == '0': #fills board w/ tiles
                board[row][col] = square
            
            print(board[row][col], end = '   ')
            
            if col == 14: #prints new line for each row
                print()

def place_word(word, direction, place_point, p_hand): #places word on board
    x = place_point[0]
    y = place_point[1]
    
    hand = check_play(word, direction, place_point, p_hand)
    c_word = check_spelling(word, hand[1])
       
    if hand[0] == False or c_word == False:
        return False #word is not playable
    
    else:
        
        hand = hand[1] #hand = player hand, now with needed letters
    
        if direction == "right":
            for letter in word:
                board[y][x] = letter
                x += 1
                
        if direction == "down":
            for letter in word:
                board[y][x] = letter
                y += 1
        
        for letter in word:
            hand.remove(letter)
        
        draw_board()
        
        return hand

def check_play(word, direction, place_point, p_hand):
    x = place_point[0]
    y = place_point[1]
    
    needed_letters = [] #list of letters player is using from board

    num = len(word)
    
    if direction == 'right':        
        for i in range(num):
            letter = word[i]
            if board[y][x + i] == letter: #checks for which letter(s) player are using that are already on the board
                needed_letters.append(letter) 
                
    elif direction == 'down':        
        for i in range(num):
            letter = word[i]
            if board[y + i][x] == letter:
                needed_letters.append(letter)
    
    if len(needed_letters) == 0: #runs if letter player needs is not on the board
        return (False, [0])
    
    else: 
        for letter in needed_letters:
            p_hand.append(letter)      
        return (True, p_hand)
    
def check_spelling(word, p_hand): #checks validity of user's played word
    # if dict.check(word) == False: #checks if word exists in english dictionary
    #     print("Invalid word.")
    #     return False
    
    hand = [] #copy of p_hand
    
    for letter in p_hand:
        hand.append(letter)
    
    for letter in word:
        if letter in hand:
            hand.remove(letter)
        else:
            return False
        
    return True

def play_first(word, direction, place_point, hand): #runs only for first turn (special condition)
    x = place_point[0]
    y = place_point[1]
    
    list_x = []
    list_y = []
    
    #checks if first turn runs through centre (7, 7)
    if (direction == "right" and y != 7) or (direction == "right" and (x > 7 or x + len(word) < 8)):
        return False
    
    elif (direction == "down" and x != 7) or (direction == "down" and (y > 7 or y + len(word) < 8)):
        return False
    
    elif direction == "right":
        j = y
        for i in range(len(word)):
            list_y.append(j)
            j += 1
        if 7 not in list_y:
            return False
        
    elif direction == 'down':
        j = x
        for i in range(len(word)):
            list_x.append(j)
            j += 1
        if 7 not in list_x:
            return False
    
    if check_spelling(word, hand) == True:
   
        if direction == "right":
            for letter in word:
                board[y][x] = letter
                x += 1
                
        if direction == "down":
            for letter in word:
                board[y][x] = letter
                y += 1
        
        for letter in word:
            hand.remove(letter)
        
        draw_board()
        
        return hand
    
    else:
        
        return False
    
def check_borders(word, direction, place_point): #checks if word falls within borders of board
    x = place_point[0]
    y = place_point[1]
    
    if direction == "right":
        if x + len(word) > 15:
            return False
    
    elif direction == "down":
        if y + len(word) > 15:
            return False
    
    return True

def plot_points(points1, points2, round_num): #graphs player results
    graph = plt.subplot()
    
    x_values = ["Player 1", "Player 2"]
    y_values = [points1, points2]
    width = 0.5
    
    graph.bar(x_values[0], y_values[0], width, color = "r")
    graph.bar(x_values[1], y_values[1], width, color = "b")
    
    graph.set_xlabel("Players")
    graph.set_ylabel("Player Score")
    plt.title("Scores for round: " + str(round_num))
    
    plt.show()