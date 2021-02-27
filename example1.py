from flask import Flask, request, redirect
import time
import random
class MultiplayerGame:

        def __init__(self, gameId, wordStart):
                self.gameId = gameId
                self.wordStart = wordStart

                self.gameDict = {}
        def addGame(self, game):

                self.gameDict[game.username] = game
                game.wordStart = self.wordStart
class WordGame:


        def __init__(self, gameLength, gameId, username, goodWords = None, wordStart = None):
                self.wordStart = wordStart
                self.startTime = time.time()
                self.gameLength = gameLength
                self.goodWords = goodWords
                self.gameId = gameId
                self.words = []
                self.username = username

        def getGameTime(self):

                return time.time() - self.startTime

        def getSecondsLeft(self):

                return int(max(self.startTime + self.gameLength - time.time(), 0))

        def gameNotOver(self):

                return self.getGameTime() < self.gameLength

        def addWord(self, word):

                if self.gameNotOver():

                        word = self.processWord(word)

                        if self.checkWord(word):

                                self.words.append(word)

        def processWord(self, word):

                word = word.lower()

                word = word.strip()

                return word


        def checkWord(self, word):
                if word is None:
                        return False

                if len(word) == 0:

                        return False

                if " " in word:
                        return False
                
                if word in self.words:
                        return False

                if self.goodWords is None:
                        return True
        
                return word in self.goodWords


        def getWords(self):
                wordStr = ""

                for j in self.words:


                        wordStr += "<p>" +  j  + "</p>"
                return wordStr

        def getInfo(self):
                if not self.gameNotOver():
                        return "<p> Peli on päättynyt </p>"

                return ""

        def getScore(self):
                return "<p> Olet keksinyt %s sanaa </p>" % len(self.words)

        def getInstruction(self):

                return "<p>Lisää %s-alkuisia sanoja </p>" % self.wordStart

games = {}
multiGames = {}

words = []


'''
filename = wordStart + '.txt'

goodWords = []



with open(filename, 'r') as f:

        text = f.read()
        text = text.replace('\xad', '')
        print(text)        
        goodWords = text.split('\n')[: -1]

        print(goodWords)'''



wordStartList = ['saa']

filename = 'tavu.txt'


with open(filename, 'r') as f:

        text = f.read()
        text = text.replace('\xad', '')
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        wordStartList = text.split(', ')

print(wordStartList)

wordStart = random.choice(wordStartList)

def getWords(gameId):

        wordStr = ""

        for j in games[gameId].words:


                wordStr += "<p>" +  j  + "</p>"
        return wordStr

def info(gameId):
        if not games[gameId].gameNotOver():
                return "<p> Peli on päättynyt </p>"

        return ""

def getScore(gameId):

        return "<p> Olet keksinyt %s sanaa </p>" % len(games[gameId].words)

def instruction():

        return "<p>Lisää %s-alkuisia sanoja </p>" % wordStart


def showResults(game):
        '''
        if game.gameNotOver:
                return ""'''

        
        return "<button type='button' onclick=\"window.location.href='/game/%s/results'\"> Tulokset</button>" % game.gameId


app = Flask(__name__)
#<input type=\"submit\" value=\"Lisää sana\"/>



@app.route("/")
def sanasaurus():
        return "Sanasaurus" + "<form action='/newgame' method=\"post\"><input type='submit' value='Luo uusi peli' id='new_game'>  </form>"


@app.route("/newgame", methods=["POST"])
def newGame():
        gameId = str(len(games))

        '''
        game = WordGame(goodWords, gameId, 120)

        games[gameId] = game'''
        
        multi = MultiplayerGame(gameId, random.choice(wordStartList))

        multiGames[gameId] = multi
        

        return redirect("/game/%s" % gameId)


@app.route("/game/<gameId>/user/<username>/submit", methods=["GET", "POST"])
def submitWord(gameId, username):
        if 'word' in request.form:
                inputWord = request.form['word']


                multiGames[gameId].gameDict[username].addWord(inputWord)

                '''
                inputWord = inputWord.lower()
                
                if len(inputWord) >= len(wordStart) and inputWord[:len(wordStart)] == wordStart and inputWord not in words and inputWord in goodWords:
                        words.append(inputWord)'''

        print(list(request.form.items()))
        return redirect("/game/%s/user/%s" % (gameId, username))

'''
@app.route("/game/<gameId>", methods =["GET"])
def showGame(gameId):
        print(gameId)
        return "<div id='timer_div'> </div>" + instruction() + getScore(gameId) + info(gameId) + "<form action='/game/%s/submit' method=\"post\"><input type=\"text\" name=\"word\"  autocomplete='off' id=\"wordInput\">  </form>" % gameId + getWords(gameId) +"<script>window.onload = function() { document.getElementById(\"wordInput\").focus();}; var seconds_left = %d;document.getElementById('timer_div').innerHTML = seconds_left; var interval = setInterval(function() {document.getElementById('timer_div').innerHTML = --seconds_left; if (seconds_left <= 0) { document.getElementById('timer_div').innerHTML = 0; clearInterval(interval);}}, 1000);</script>" % games[gameId].getSecondsLeft()'''

@app.route("/game/<gameId>", methods =["GET"])
def showMultiplayerGame(gameId):

        if gameId not in multiGames:

                return redirect("/")

        playerString = "<p> Pelaajat: </p>"

        for j in multiGames[gameId].gameDict.keys():

                playerString += "<p>" + j + "</p>"

        return "<form action = '/game/%s/newplayer' method='post'><label> Nimesi</label><input type='text' autocomplete='off' name='username' id='username_input' ><input type='submit' value='Aloita peli' ></form>" % gameId + playerString

@app.route("/game/<gameId>/newplayer", methods = ["POST"])
def redirectUserToGame(gameId):
        if gameId not in multiGames:

                return redirect("/")


        username = request.form['username']

        if len(username) == 0:
                return redirect("/game/%s" % gameId)

        gameLength = 30
        game = WordGame(gameLength, gameId, username)

        multiGames[gameId].addGame(game)

        return redirect("/game/%s/user/%s" % (gameId, username))

@app.route("/game/<gameId>/user/<username>", methods =["GET"])
def showPlayerWordGame(gameId, username):

        if gameId not in multiGames:

                return redirect("/")

        if username not in multiGames[gameId].gameDict:
                return redirect("/game/%s" % gameId)


        game = multiGames[gameId].gameDict[username]
        if game.gameNotOver():
                refreshInd = "true"
        else:
                refreshInd = "false"
        return "<div id='timer_div'> </div>" + game.getInstruction() + game.getScore() + game.getInfo() + "<form action='/game/%s/user/%s/submit' method=\"post\"><input type=\"text\" name=\"word\"  autocomplete='off' id=\"wordInput\">  </form>" % (gameId, username) + game.getWords() + showResults(game) +"<script>function display (seconds) {const format = val => `0${Math.floor(val)}`.slice(-2);const hours = seconds / 3600;const minutes = (seconds % 3600) / 60;return [hours, minutes, seconds % 60].map(format).join(':');}</script>" +"<script>window.onload = function() { document.getElementById(\"wordInput\").focus();}; var seconds_left = %d; var refresh = %s; document.getElementById('timer_div').innerHTML = display(seconds_left); var interval = setInterval(function() {document.getElementById('timer_div').innerHTML = display(--seconds_left); if (seconds_left <= 0) { document.getElementById('timer_div').innerHTML = display(0); clearInterval(interval); if (refresh) {window.location.reload();} }}, 1000);</script>" % (game.getSecondsLeft(), refreshInd)

@app.route("/game/<gameId>/results")
def results(gameId):
        if gameId not in multiGames:

                return redirect("/")

        playerString = "<p> Tulokset: </p>"

        for j in multiGames[gameId].gameDict.keys():
                w = multiGames[gameId].gameDict[j].words
                playerString += "<div><p>" + j + ": " + str(len(w)) + "</p>" + "<p><small>" + ", ".join(w) + "</small></p>" + "</div>"  

        return playerString

if __name__ == "__main__":
        app.run()
