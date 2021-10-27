"""A flask application that gives you picture of a cocktail, its name, and what glass to serve it in."""

import requests
from os import getenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

cocktail_app = Flask(__name__)
cocktail_app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
cocktail_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(cocktail_app)


@cocktail_app.route("/")
def index():
    # Querying from database
    main_query = Cocktails.query.all()

    cocktail_names = []
    cocktail_glasses = []
    cocktail_pictures = []

    for i, query in enumerate(main_query):
        loop_query = main_query[i]
        query_name = loop_query.name
        query_glass = loop_query.glass_type
        query_picture = str(loop_query)
        cocktail_names.append(query_name)
        cocktail_glasses.append(query_glass)
        cocktail_pictures.append(query_picture)

    return render_template(
        "index.html", cocktail_name0=cocktail_names[0], cocktail_glass0=cocktail_glasses[0],
        cocktail_image0=cocktail_pictures[0],
        cocktail_name1=cocktail_names[1], cocktail_glass1=cocktail_glasses[1], cocktail_image1=cocktail_pictures[1],
        cocktail_name2=cocktail_names[2], cocktail_glass2=cocktail_glasses[2], cocktail_image2=cocktail_pictures[2],
        cocktail_name3=cocktail_names[3], cocktail_glass3=cocktail_glasses[3], cocktail_image3=cocktail_pictures[3],
        cocktail_name4=cocktail_names[4], cocktail_glass4=cocktail_glasses[4], cocktail_image4=cocktail_pictures[4]
    )


@cocktail_app.route("/reset")
def reset():
    db.drop_all()
    db.create_all()
    return "Database reset!"


@cocktail_app.route('/add-moscow-mule')
def add_moscow_mule():
    request = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=moscow")
    mos_mule_json = request.json()
    mos_mule_data = list((mos_mule_json["drinks"])[0].values())
    mos_mule_name = mos_mule_data[1]
    mos_mule_glass = mos_mule_data[8]
    mos_mule_picture = mos_mule_data[16]
    record_mm = Cocktails(
        name=mos_mule_name, glass_type=mos_mule_glass, picture=mos_mule_picture
    )
    db.session.add(record_mm)
    db.session.commit()
    return "Moscow mule added!"


@cocktail_app.route('/add-munich-mule')
def add_munich_mule():
    request = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=munich")
    mun_mule_json = request.json()
    mun_mule_data = list((mun_mule_json["drinks"])[0].values())
    mun_mule_name = mun_mule_data[1]
    mun_mule_glass = mun_mule_data[8]
    mun_mule_picture = mun_mule_data[16]
    record_munm = Cocktails(
        name=mun_mule_name, glass_type=mun_mule_glass, picture=mun_mule_picture
    )
    db.session.add(record_munm)
    db.session.commit()
    return "Munich mule added!"


@cocktail_app.route('/add-aperol-spritz')
def add_aperol_spritz():
    request = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=aperol")
    aperol_json = request.json()
    aperol_data = list((aperol_json["drinks"])[0].values())
    aperol_name = aperol_data[1]
    aperol_glass = aperol_data[8]
    aperol_picture = aperol_data[16]
    record_aperol = Cocktails(
        name=aperol_name, glass_type=aperol_glass, picture=aperol_picture
    )
    db.session.add(record_aperol)
    db.session.commit()
    return "Aperol spritz added!"


@cocktail_app.route('/add-frisco-sour')
def add_frisco_sour():
    request = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=frisco")
    frisco_json = request.json()
    frisco_data = list((frisco_json["drinks"])[0].values())
    frisco_name = frisco_data[1]
    frisco_glass = frisco_data[8]
    frisco_picture = frisco_data[16]
    record_frisco = Cocktails(
        name=frisco_name, glass_type=frisco_glass, picture=frisco_picture
    )
    db.session.add(record_frisco)
    db.session.commit()
    return "Frisco sour added!"


@cocktail_app.route('/add-mulled-wine')
def add_mulled_wine():
    request = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=mulled")
    mlwine_json = request.json()
    mlwine_data = list((mlwine_json["drinks"])[0].values())
    mlwine_name = mlwine_data[1]
    mlwine_glass = mlwine_data[8]
    mlwine_picture = mlwine_data[16]
    record_mlwine = Cocktails(
        name=mlwine_name, glass_type=mlwine_glass, picture=mlwine_picture
    )
    db.session.add(record_mlwine)
    db.session.commit()
    return "Mulled wine added!"


# Create Cocktail table using SQLAlchemy
class Cocktails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    glass_type = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return self.picture
