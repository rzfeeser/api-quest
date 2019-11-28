#!/usr/bin/python3
"""Welcome to Alta3 Web RPG"""

## standard library
import json

## flask imports
from flask import Flask
from flask import session
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

## parsing user commands
# parse out get commands
from usercommands import get
# parse out go commands
from usercommands import go

"""
Flask Sessions are leveraged to store encrypted cookie data, the player's state, on the client side.

API endpoints:

   /new/ - start a new game
   
   /status/ - return the current status of the player

   /go/<direction> - attempt to move in a direction

   /get/<item> - attempt to pick up an item

   /help/ - return help
   
"""

# create the world object
with open("world.json", "r") as world:
    rooms = json.load(world)


app = Flask(__name__)
app.secret_key = "rzfeeser:RAND"


# start a new game
@app.route("/", methods = ["POST", "GET"])
@app.route("/new/", methods = ["POST", "GET"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        ans = request.form.get("neworcontinue") # indicated by a button click
        if ans == 'newgame' or not session.get("currentRoom"): # or not session.get("inventory"): # not necessary???
            session.clear()   # if "Yes", clear the session cookie
            session["rooms"] = rooms # load the new game with newest world data
            session["currentRoom"] = "Hall"  # set the location as the Hall
            session["inventory"] = [] # cast inventory as an empty list
            session["turnno"] = 0 # number of moves taken
        return redirect(url_for("status")) # in all cases, move the user to status


# endpoint for status
# always called at start of turn
@app.route("/status/", methods = ["POST", "GET"])
def status():
    if request.method == "GET":
        status = {}
        # Return your current room
        # check if user had a new game spawned or they cut right to /status/
        if session.get('currentRoom'):
            status['currentRoom'] = session['currentRoom']
        else:
            redirect(url_for("new"))

        # Return your inventory
        status['inventory'] = session.get('inventory')

        # If you met the objectives of the game
        # 1) you have the potion
        # 2) you have the skeleton key
        if session.get("currentRoom") == "Garden":
            if 'skeleton key' in session.get('inventory') and 'potion' in session.get('inventory'):
                return redirect(url_for("gameover", endreason="""You enter the garden, and unlock the rusty gate with
                the skeleton key!\nYou win!"""))
            else:
                session["turnresult"] = "You'd win if you only had a few more items..."

        # An item is in the room you are in
        if 'item' in session.get('rooms')[session.get('currentRoom')]:
            status['item'] = session.get('rooms')[(session['currentRoom'])]['item'] # set it within the json
            ## monster check
            if status['item'] == 'monster' and "spell book" in session.get('inventory'):
                session['rooms'][session.get('currentRoom')].pop('item', None) # remove the key item from dictionary
                session['inventory'].remove("spell book") # remove the item "spell book" from the list
                session['turnresult'] = "You walk into a dark room. A grue is here. As it approaches you, the spell book falls from your pouch and opens to a page with charcoal drawings of cryptic runes and a drawing of a latern. Bright light suddenly beams from the book eviserating the Grue."
            elif status['item'] == 'monster':
                return redirect(url_for("gameover", endreason="""There is a hungry Grue here! And you're invited to be
                dinner!"""))
        else:
            status['item'] = None

        # The current turn
        status['turnno'] = session.get('turnno')
        # Results of last turn
        status['turnresult'] = session.get('turnresult')

        return render_template("status.html", **status) # return the status
    
    # Process the user response
    if request.method == "POST":
    
        if request.form.get("playermove"):
            playermove = request.form.get("playermove")
            ## split to allow for compound words, like "get skeleton key"
            playermove = playermove.lower().split(" ", 1) # only split on the first whitespace

            if playermove[0] == "go": # if the user typed 'go'
                session["turnresult"] = go(rooms, playermove[1], session.get("currentRoom"))
            elif playermove[0] == "get": # if the user typed 'get'
                session["turnresult"] = get(playermove[1], session.get("currentRoom"))
            elif playermove[0] == "help": # if the user typed 'help'
                session["turnresult"] = gamehelp()
            else:
                session["turnresult"] = "I am not sure what you are trying to do."
            
            session["turnno"] += 1  # increase the number of moves
     
        return redirect(url_for("status"))



@app.route("/gameover/<endreason>", methods=["GET"])
def gameover(endreason):
    if request.method == "GET":
        session.clear()  # delete the user's session cookie
        if "win" in endreason:
            return render_template("win.html", endreason=endreason)
        else:
            return render_template("gameover.html", endreason=endreason)

if __name__ == "__main__":
    app.run(port=5006)