from flask import Flask, render_template, request, redirect, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

def get_province_names():
    provinces = []
    for province in mongo.db.collection_names():
        if not province.startswith("system."):
                province.append(province)
    return provinces

@app.route("/")
def show_home():
    return render_template("home.html")
    
@app.route("/scores/<province>")
def show_entries_by_province(province):
    entries = mongo.db[province].find()
    return render_template("scores.html", entries = entries)
    
@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
    return render_template("add_entry.html")
    
    
    
    
    
    
if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)