from flask import Flask, render_template, request
import sqlite3 as sql
import datetime

from subprocess import call
app = Flask(__name__,template_folder='./')  

call(["python3", "setup.py"])

@app.route('/')
def home():
    return render_template('home.html') 
    
@app.route('/games')
def games():
    return render_template('pyGames.html')
    
@app.route('/Galaga')
def pyGalaga():
    call(["python3", "pyGal.py"])
    return render_template('pyGal.html') 
    
@app.route('/addReview')
def new_review():
    return render_template('reviewAdder.html')

@app.route('/',methods = ['GET', 'POST'])
def addr():
    if request.method == 'POST':
        try:
            user = request.form['Username']
            game = request.form['Game']
            rates = request.form['Rating']
            reviews = request.form['Review']
            rate = float(rate)
            with sql.connect("reviewData.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Reviews (Username, Game, ReviewTime, Rating, Review) VALUES (?,?,?,?,?)", (user,game,datetime.datetime.now(),rates,reviews) )  
                con.commit()
        except:
            con.rollback()
        
        finally:
            return render_template('home.html')  
            con.close()
    
    
if __name__ == '__main__':
    app.run(debug = True)
