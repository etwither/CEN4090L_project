from flask import Flask, render_template, request
import sqlite3 as sql
import datetime

from subprocess import call
app = Flask(__name__,template_folder='./')  

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
    
if __name__ == '__main__':
    app.run(debug = True)
