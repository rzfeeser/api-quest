#!/usr/bin/python3
#from flask import redirect
#from flask import url_for


"""This file contains all of the rooms logic
functions should match the name of rooms in world.json made lowercase and stripped of whitespace"""
def roomlogic(currentroom):
    ## garden logic
    def garden(session):
        if 'skeleton key' in session.get('inventory'):
            # x = lambda: redirect(url_for("gameover", endreason="win", endcode="1"))
            return ("gameover", "win", "1")
        else:
            session["turnresult"] = "You'd win if you only had a few more items..."
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
    if currentroom == "Garden":
        return garden
    elif currentroom == "Hall":
        return hall
    elif currentroom == "Dining Room":
        return diningroom
    elif currentroom == "Library":
        return library
    elif currentroom == "Kitchen":
        return kitchen