#This is the code for a 5 wheel, 3 visible tiles per wheel slot machine game. The machine is implemented in a series of
#functions, each of which is designed to deal with various aspects of the game. The important feature from a game design
#perspective is that the "distribution of tiles on a wheel" and "payouts per tile", and "win shapes" are each independent
#arrays, enabling complete customisation of these to obtain a desired payout. The ones provided here are not mathematically
#tested, beyond the authors intuition.

import numpy as np
import random

#These functions deal with the mechanics of moving a wheel, represented as an array (spin and shift are the same, except spin
#is random, and shift is by one tile.
def spin(a):
    b=[]
    N=random.randint(0,len(a))
    for i in range(len(a)):
        b.append(a[(i+N)%len(a)])
    return b

def shift(a):
    b=[]
    for i in range(len(a)):
        b.append(a[(i+1)%len(a)])
    return b

#the following function allows us to visualise a given state more clearly than an array of 5 arrays.
def window(a, n=5, k=3):
    w = np.array([i[0:k] for i in a[0:n]])
    v=w.T
    str_v=["|".join([" %d " % x for x in v[i]]) for i in range(len(v))]
    return '\n'.join(str_v)

#This is "pulling the lever", or obtaining a random state for the machine.
def pull(b):
    b = np.array([spin(b[i]) for i in range(len(b))])
    return b

# a wheel generator for a distribution (maths will be by hand, not yet completed)

distribution = [482, 241, 122, 62, 32, 16, 45]
alphabet = [x for x in range(len(distribution))]

def wheel(a=distribution, b=alphabet):
    wheel_list = [[b[i] for x in range(a[i])] for i in range(len(a))]
    wheel = []
    for i in range(len(wheel_list)):
        wheel = wheel + wheel_list[i]
    random.shuffle(wheel)
    return wheel

#state detection for win conditions

#This will be the vector of payouts for the different tiles:
#this needs to be an accessible point of control, since
#combined with the distribution going in it defines the overall payout

def tile_value(a, i, j):
    #the tile payouts array is really replacable with whatever values you want
    #I used probabilities that were increasing fractions of powers of 2 (dyadics)
    #and so I chose values that were powers of 2.
    tile_payouts = np.exp2(alphabet)
    tile_payouts[0]=1
    for k in alphabet:
        if a[i][j]==k:
            return int(tile_payouts[k])

#This will be the function that tests shapes and assigns a value from shape_values, adjusts spins, nudges, etc.

def shape(a):
#This array should contain values for the shapes you want to have as win conditions.
#This should relate to the probability of that occuring, but I haven't sat and done that math yet
#so I have placeholders to test the output.
    shape_values = np.exp2([1,2,3,4,5,6,7,8])

    #B_1
    if a[0][1]==a[1][1]==a[2][1]==a[3][1]==a[4][1]:
            payout = int(shape_values[0])*tile_value(a,0,1)
    #A
    elif a[0][0]==a[1][0]==a[2][1]==a[3][2]==a[4][2]:
            payout = int(shape_values[1])*tile_value(a,0,0)
        #C
    elif a[1][0]==a[1][2]==a[3][0]==a[3][2]:
            payout = int(shape_values[2])*tile_value(a,1,0)
        #D
    elif a[0][2]==a[1][2]==a[2][1]==a[3][0]==a[4][0]:
            payout = int(shape_values[3])*tile_value(a,0,2)
        #E
    elif a[0][0]==a[0][2]==a[2][0]==a[2][2]==a[4][0]==a[4][2]:
            payout = int(shape_values[4])*tile_value(a,0,0)
        #F
    elif a[0][1]==a[4][1]==a[1][0]==a[1][2]==a[3][0]==a[3][2]:
            payout = int(shape_values[5])*tile_value(a,0,1)
        #G
    elif a[0][1]==a[1][1]==a[0][2]==a[1][2]:
            payout = int(shape_values[6])*tile_value(a,0,1)
        #H
    elif a[3][0] == a[3][1] == a[4][0] == a[4][1]:
            payout = int(shape_values[7])*tile_value(a,3,0)
    else:
        payout = 0
    return payout

#The following is the game itself, with a variety of actions.
def machine(state=np.array([range(10),range(10),range(10),range(10),range(10)])):
    #To add: making a wildcard. Not implemented yet. No declaration of winning shapes, but they are encoded.
    spins=5
    state=pull(state)
    print("Welcome to the 5x3 math test slots!")
    rules = input("Do you want the rules (y/n)?")
    if rules == "y":
        print(
            "This is a slot machine with 5 wheels, the wheels have symbols 0 to 7 printed on them. \n"
            "You can fix wheels, swap pairs of wheels, and nudge, but these cost 1 spin per action. \n"
            "You start with 5 spins. Good luck!"
        )
    print(window(state))
    pay=shape(state)
    print("You have", spins, "spins remaining. Currently this is worth", pay, "value.")
    play = input("Do you want to spin (y), fix some wheels and spin (f), swap rows (sw), nudge (n) or stop (s)?")

    while play != 0:
        #Complete respin
        if play == "y":
            state=pull(state)
            print(window(state))
            spins=spins-1
            if spins !=0:
                pay = shape(state)
                print("You have", spins, "spins remaining. Currently this is worth", pay, "value.")
                play = input("Do you want to spin (y), fix some wheels and spin (f), swap rows (sw), nudge (n) or stop (s)?")
            if spins == 0:
                play = 0
                pay = shape(state)
        #Spinning fixing some rows
        elif play == "f":
            fix = [int(x)-1 for x in input("Which wheels would you like to fix?").split(",")]
            if fix == []:
                fix = [int(x)-1 for x in input("Oops, you didn't enter any wheels, which wheels would you like to fix?").split(",")]
            elif fix != []:
                for i in [x for x in range(len(state)) if x not in fix]:
                    state[i]=spin(state[i])
            print(window(state))
            spins = spins - 1
            if spins != 0:
                pay = shape(state)
                print("You have", spins, "spins remaining. Currently this is worth", pay, "value.")
                play = input("Do you want to spin (y), fix some wheels and spin (f), swap rows (sw), nudge (n) or stop (s)?")
            if spins == 0:
                play = 0
                pay = shape(state)
        elif play == "sw":
            swap = [int(x)-1 for x in input("Which two rows do you want to swap?").split(",")]
            state[[swap[0],swap[1]]]=state[[swap[1],swap[0]]]
            print(window(state))
            spins = spins-1
            if spins != 0:
                pay = shape(state)
                print("You have", spins, "spins remaining. Currently this is worth", pay, "value.")
                play = input("Do you want to spin (y), fix some wheels and spin (f), swap rows (sw), nudge (n) or stop (s)?")
            if spins == 0:
                play = 0
                pay = shape(state)
        elif play == "n":
            nudge = int(input("Which row would you like to nudge up one tile?"))-1
            state[nudge] = shift(state[nudge])
            print(window(state))
            spins = spins - 1
            pay = shape(state)
            if spins != 0:
                print("You have", spins, "spins remaining. Currently this is worth", pay, "value.")
                play = input("Do you want to spin (y), fix some wheels and spin (f), swap rows (sw), nudge (n) or stop (s)?")
            if spins == 0:
                play = 0
                pay = shape(state)
        #Exit
        elif play =="s":
            play = 0
            pay = shape(state)
        elif play != "s" or play != "sw" or play != "n" or play != "f" or play != "y":
            print("Oops, I don't recognise that choice.")
            play = input("Do you want to spin (y), fix some wheels and spin (f), swap rows (sw), nudge (n) or stop (s)?")
    return print("You won", pay, ". Thanks for playing!")

machine_wheel = wheel(distribution,alphabet)
state=np.array([machine_wheel,machine_wheel,machine_wheel,machine_wheel,machine_wheel])

#Running the script will start the game, comment to stop that behaviour.
machine(state)