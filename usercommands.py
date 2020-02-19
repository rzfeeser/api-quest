#!/usr/bin/python3

from flask import session

# user type attack
# user types use
# user types drop

# user types help
def gamehelp():
    return '''
    Welcome to api-quest!
    
    api-quest is a text parsing adventure inspired by Infocom games of the 80s.    
    
    Try to stay out of the dark, else you'll be eaten by a grue.
    

    RPG GAME
    ========
    Commands:
      go [direction]
      get [item]
      look
      help
    '''


# user types go
def go(rooms, direction, currentRoom):
    if direction in rooms[currentRoom]:
        session["currentRoom"] = rooms[currentRoom][direction]
        return f"You moved {direction}. {rooms.get(rooms[currentRoom][direction]).get('desc')}"
    else:
        return f"You cannot move {direction}."

# user types get kitkat (user tries to pick something up)
def get(kitkat, currentRoom):
    if 'item' in session.get('rooms')[currentRoom]: # does the room have an item to be picked up?
        for oneword in session.get('rooms')[currentRoom]['item'].split(): # the item maybe a compound word so split it
            if kitkat == session.get('rooms')[currentRoom]['item'] or oneword == kitkat: # abbreviation matching EX: "skeleton" and "key" would match "skeleton key"
                ## session['inventory'] += [kitkat]  # NO! This results in a user adding a single word to their inventory
                                                     # ex: if a skeleton key is in the room and they type 'get key' they
                                                     # end up with 'key' added to inventory
                kitkat = session.get('rooms')[currentRoom]['item']  ## standardize kitkat from user session data
                session['inventory'].append(kitkat) # add item from world.json to inventory
                session['rooms'][currentRoom].pop('item', None)
                session.modified = True # always do this after modifying a session
                return f"{kitkat} picked up!"
    # if you made it this far, your pickup logic didn't work out
    return f"You cannot pickup {kitkat}."

# user types look
def look(rooms, currentRoom):
    return f"{rooms.get(currentRoom).get('desc')}"

# user types use
# example: use potion
# example: use potion on wound
# example: use feather in potion
# example: use knife with jelly
def use(currentRoom):
    pass