#!/usr/bin/python3
#from flask import redirect
#from flask import url_for


"""This file contains all of the rooms logic
functions should match the name of rooms in world.json made lowercase and stripped of whitespace"""
def roomlogic(currentroom):
    ## garden logic
    def garden(session):
        if 'skeleton key' in session.get('inventory'):
            session["turnresult"] = "The skeleton key opens the gate! But the key is now stuck in the lock."
            session['inventory'].remove('skeleton key')
            if session['rooms'].get('garden', {}).get('item') == 'gate':
                session['rooms']['garden'].pop('item', None)
            session['rooms']['garden']['south'] = 'maze'
            session.modified = True
            return
        else:
            session["turnresult"] = "You are in the garden and the gate appears locked"
            return

    ## library logic
    def library(session):
        pass

    ## hall logic
    def hall(session):
        pass

    ## diningroom logic
    def diningroom(session):
        pass

    ## kitchen logic
    def kitchen(session):
        if session.get('rooms')[(session['currentRoom'])].get('item') == 'monster' and "spell book" in session.get('inventory'):    ## monster check
            session['rooms'][session.get('currentRoom')].pop('item', None)  # remove the key item from dictionary
            session['inventory'].remove("spell book")  # remove the item "spell book" from the list
            session['turnresult'] = "You walk into a dark room. A grue is here. As it approaches you, the spell book \
              falls from your pouch and opens to a page with charcoal drawings of cryptic runes and a drawing of a \
              latern. Bright light suddenly beams from the book eviserating an approaching Grue. As the ghastly \
              creature fades into the etheral plane, a small white feather appears and floats to the ground."
            session['rooms'][session.get('currentRoom')]['item'] = 'white feather'
            session.modified = True  # always do this after modifying a session
            return
        elif session.get('rooms')[(session['currentRoom'])].get('item') == 'monster':
            return ("gameover", "lost", "1")

    ## bust down the currentroom
    if currentroom == "garden":
        return garden
    elif currentroom == "hall":
        return hall
    elif currentroom == "dining room":
        return diningroom
    elif currentroom == "library":
        return library
    elif currentroom == "kitchen":
        return kitchen
    else:
        def noop(session):
            #session["turnresult"] = f"You are in {currentroom}. There is nothing special here."
            return
        return noop