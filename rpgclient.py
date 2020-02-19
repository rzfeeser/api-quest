#!/usr/bin/python3
"""Working on client side logic for API RPG game
   Just making sure github desktop works!"""


import requests

import argparse


while True:
    currentstatus = requests.get(args.svrip + "/status/")
    print(currentstatus)
    move = ''
    while move == '':
        move = input('> ')
    # >
    # >
    # > go NORTH
    move = move.lower().split()
    # ['go', 'north']

    if move[0] == 'go':
        currentstatus = requests.get(args.svrip + "/go/" + move[1])

    elif move[0] == 'get':
        currentstatus = requests.get(args.svrip + "/get/" + move[1])

    elif move[0] == 'help':

    elif move[0] == 'status':

    else:
        print("That is not a command I understand.")


if __name__ == "__main__":
