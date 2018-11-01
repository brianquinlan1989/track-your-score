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
                provinces.append(province)
    return provinces

@app.route("/")
def show_home():
    return render_template("home.html", provinces=["Leinster", "Munster", "Connacht", "Ulster"])
    
@app.route("/scores/<province>")
def show_entries_by_province(province):
    entries = mongo.db[province].find()
    provinces = get_province_names()
    return render_template("scores.html", entries = entries, provinces = provinces, province = province)
    
@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        form_entries = request.form.to_dict()
        province = form_entries["province"]
        mongo.db[province].insert_one(form_entries)
        return redirect("/scores/"+province)
    else:
        provinces = get_province_names()
        return render_template("add_entry.html", provinces=provinces)

    
    
    
if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)