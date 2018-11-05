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
        form_entries["net_score_name"] = int(request.form["gross_score_name"]) - int(request.form["handicap_name"])
        province = form_entries["province_name"]
        mongo.db[province].insert_one(form_entries)
        return redirect("/scores/"+province)
    else:
        provinces = get_province_names()
        return render_template("add_entry.html", provinces=provinces)
        
@app.route("/scores/<province>/<entry_id>/edit", methods=["GET", "POST"])
def edit_entry(province, entry_id):
    if request.method == "POST":
        form_entries = request.form.to_dict()
        mongo.db[province].update({"_id": ObjectId(entry_id)}, form_entries)
        
        if form_entries["province_name"] != province:
            the_entry = mongo.db[province].find_one({"_id": ObjectId(entry_id)})
            mongo.db[province].remove(the_entry)
            mongo.db[form_entries["province_name"]].insert(the_entry)
            
        return redirect(
            url_for("show_entries_by_province", province=form_entries["province_name"]))
        
    else:
        the_entry = mongo.db[province].find_one({"_id": ObjectId(entry_id)})
        provinces = get_province_names() 
        return render_template("edit_entry.html", entry=the_entry, provinces=provinces)

@app.route("/scores/<province>/delete", methods=["POST"])
def delete_entry(province):
    id_to_delete = request.form['entry_id']
    print(id_to_delete)
    mongo.db[province].remove({"_id":ObjectId(id_to_delete)})
    return redirect(url_for("show_entries_by_province", province=province))
    # return "Test"
  
    
if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)