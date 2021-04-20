from flask import Flask, render_template, request
import sqlite3 as sql
import datetime

from subprocess import call
app = Flask(__name__,template_folder='./')  

#call(["python3", "startDatabase.py"])

@app.route('/')
def home():
    return render_template('home.html') 
    
@app.route('/games')
def games():
    return render_template('pyGames.html')
    
@app.route('/EscapeArtist')
def escape():
    call(["python3", "eaplay.py"])
    return render_template('escape.html')
    
@app.route('/Galaga')
def pyGalaga():
    call(["python3", "pyGal.py"])
    return render_template('pyGal.html')
    
@app.route('/Pacman')
def pacman():
    call(["python3", "pacman_main.py"])
    return render_template('pacman.html') 
    
@app.route('/Pokemon')
def pokemon():
    call(["python3", "main.py"])
    return render_template('pokemon.html') 
    
@app.route('/addReview')
def new_review():
    return render_template('reviewAdder.html')

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
            return render_template('pyGames.html')
            con.rollback()
            
        
        finally:
            return render_template('home.html')  
            con.close()

@app.route('/reviewSearch')                                       
def search_review():
    return render_template('reviewSearch.html')
    
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
    
if __name__ == '__main__':
    app.run(debug = True)
