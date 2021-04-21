from flask import Flask, render_template, request
import sqlite3 as sql
import datetime
from subprocess import call
app = Flask(__name__,template_folder='./')  #templates in the same folder as start.py

#call(["python3", "startDatabase.py"])

#opens home page
@app.route('/')
def home():
    return render_template('home.html') 

#opens game selection page
@app.route('/games')
def games():
    return render_template('pyGames.html')

#starts game and opens game info page
@app.route('/EscapeArtist')
def escape():
    call(["python3", "eaplay.py"])
    return render_template('escape.html')
    
#starts game and opens game info page
@app.route('/Galaga')
def pyGalaga():
    call(["python3", "pyGal.py"])
    return render_template('pyGal.html')
    
#starts game and opens game info page
@app.route('/Pacman')
def pacman():
    call(["python3", "pacman_main.py"])
    return render_template('pacman.html') 
    
#starts game and opens game info page
@app.route('/Pokemon')
def pokemon():
    call(["python3", "main.py"])
    return render_template('pokemon.html') 
    
#opens page to add reviews
@app.route('/addReview')
def new_review():
    return render_template('reviewAdder.html')
    
#adds new reviews into the Reviews table
@app.route('/',methods = ['GET', 'POST'])
def addr():
    if request.method == 'POST':
        try:
            un = request.form['Username']
            game = request.form['Game']
            rate = request.form['Rating']
            review = request.form['Review']
            rate = float(rate)
            with sql.connect("storeData.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Reviews (Username, Game, ReviewTime, Rating, Review) VALUES (?,?,?,?,?)", (un,game,datetime.datetime.now(),rate,review) )  
                con.commit()
        except:
            con.rollback()
            
        
        finally:
            return render_template('home.html')  
            con.close()

#opens page to search for reviews
@app.route('/reviewSearch')                                       
def search_review():
    return render_template('reviewSearch.html')
    
#gets reviews for the selected game
@app.route('/reviewsFound',methods = ['GET', 'POST'])    
def show():
    rows = []
    if request.method == 'POST':
        try:
            game = request.form['Game']        
            query = "SELECT Username,Rating,Review,ReviewTime FROM Reviews WHERE Game = '%s'" % game  
            with sql.connect("storeData.db") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute(query)                   
                rows = cur.fetchall()
        except:
            con.rollback()
        
        finally:
            return render_template("reviewsDisplay.html",rows = rows,game = game)  
            con.close()
     
#opens login page       
@app.route('/Login')
def login():
    return render_template('login.html')

#checks to see if the name and password are correct
@app.route('/removeReviews',methods = ['GET', 'POST'])
def log():
    if request.method == 'POST':
        try:
            un = request.form['Username']
            passw = request.form['Password']
            
            
        except:
            return render_template('error.html')
            
        
        finally:
            if un == 'admin':
                if passw == '12345':
                    return render_template('remove2.html')  
                else:
                    return render_template('error.html')
            else:
                return render_template('error.html')

#opens the page to remove a review
@app.route('/remove')
def rm():
    return render_template('remove.html')
                
#removes a review with the matching username and game
@app.route('/remove2',methods = ['GET', 'POST'])
def remove():
    if request.method == 'POST':
        try:
            un = request.form['Username']
            game = request.form['Game']
            q1 = "DELETE FROM Reviews WHERE (Username = '%s'" % un
            q2 = " AND Game = '%s')" % game
            query = q1 + q2
            print(query)
            with sql.connect("storeData.db") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute(query)                   
                rows = cur.fetchall()
        except:
            con.rollback()
            
        
        finally:
            return render_template('remove.html')  
            con.close()
    
if __name__ == '__main__':
    app.run(debug = True)
