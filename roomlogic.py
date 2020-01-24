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
            x = ("gameover", "win", "1") # return a tuple of what to plug in
            return x
        else:
            session["turnresult"] = "You'd win if you only had a few more items..."
            return

    ## hall logic
    def hall(session):
        pass

    ## diningroom logic
    def diningroom(session):
        pass

    ## bust down the currentroom
    if currentroom == "Garden":
        return garden
    elif currentroom == "Hall":
        return hall
    elif currentroom == "Dining Room":
        return diningroom