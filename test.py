from flask import Flask,redirect
from flask import render_template
from flask import request
import re
import datetime
import sqlite3
import models
import json
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("/index", code=302)

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "testtemp.html",
        name=name
    )

@app.route("/testarea")
def testTemp():
    return render_template(
        "index.html"
    )

@app.route("/index", methods= ['POST', 'GET'])
def index():
    if request.method == "POST":
        search = request.form['search']
        search = search.replace("", "+")
        resultBuilder = ""
        r=requests.get("https://api.elsevier.com/content/search/sciencedirect", params={"query":search,"count":"50"}, headers={"Accept":"application/json","X-ELS-APIKey":"64417dd6eed2d2f2d3aa7ca64942f679"})
        data = json.loads(r.content)
        datatwo = data['search-results']['entry']

        i = 0
        for data in datatwo:
            resultBuilder = resultBuilder + '<p><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></p>'
            i = i+1

        return render_template("results.html", search=request.form['search'], results=resultBuilder)
    return render_template(
        "index.html"
    )


@app.route('/search', methods = ['POST', 'GET'])
def search():
   if request.method == 'POST':
      try:
        #cant figure out how to get searchvalue from form passed into this searchVal variable so i hard coded it to tzit no matter .
        #what was inputted to the search box There are test records in publications and 2 of them have the word tzit somewhere in the title
        #searchVal = request.form['search']
        searchVal = request.form['search']
        con = sqlite3.connect("Users.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM publications WHERE title LIKE ?;", ("%"+searchVal+"%",))
        rows = cur.fetchall(); 
        return render_template("results.html", rows = rows)
      except:
         #redirect to home?
         print("there was an oopsy")
         return render_template("index.html")
      

        

if __name__ == '__main__':
    app.run()
