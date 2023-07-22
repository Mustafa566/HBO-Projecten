import os.path
import sqlite3
import sys

from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database
from flask_sqlalchemy import SQLAlchemy

# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "De gebruiker moet ingelogd zijn om deze pagina te bekijken"

# Secret key voor de session
app.secret_key = '1335eb3948fb7b64a029aa29'

# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')
db.init_app(app)

DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)

# Database model aanmaken voor user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# Het inladen van de users
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route("/")
def start():
    return redirect(url_for('login'))


@app.route("/index")
@login_required
def index():
    table_list = dbm.get_table_list()
    rows, column_names = dbm.get_questions_content()
    learningobjects, column_names_learning = dbm.get_learningobject_content()
    autherobjects, column_names_learning = dbm.get_authors_content()
    return render_template(
        "tables.html", rows=rows, columns=column_names, table_name='vragen', name=current_user.name,
        table_list=table_list,
        learningobjects=learningobjects, autherobjects=autherobjects
    )


@app.route("/birthFilter/", methods=['GET'])
def birthFilter():
    cursor = sqlite3.connect(DATABASE_FILE).cursor()
    rows = cursor.execute(f"SELECT * FROM auteurs WHERE geboortejaar >= 1990").fetchall()
    return rows

@app.route("/editAuteurs/<voornaam>/<achternaam>/<geboortejaar>/<medewerker>/<pensioen>/<id>", methods=['POST'])
def editAuteurs(voornaam, achternaam, geboortejaar, medewerker, pensioen, id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    rows = cursor.execute(
        f"UPDATE auteurs SET voornaam = :voornaam, achternaam = :achternaam, geboortejaar = :geboortejaar , medewerker = :medewerker, [met pensioen] = :pensioen WHERE id = :id",
        {"voornaam": "" + voornaam + "", "achternaam": achternaam, "id": id, "geboortejaar": geboortejaar, "medewerker": medewerker, "pensioen": pensioen, "id": id})
    conn.commit()

    return rows


@app.route("/deleteAuthor/<rowId>", methods=['DELETE'])
def deleteAuthor(rowId):
    id = rowId
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    rows = cursor.execute(f"DELETE FROM auteurs WHERE id = :rowId",
                          {"rowId": id})
    conn.commit()
    return []

@app.route("/deleteQuestion/<rowId>", methods=['DELETE'])
def deleteQuestion(rowId):
    id = rowId
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    rows = cursor.execute(f"DELETE FROM vragen WHERE id = :rowId",
                          {"rowId": id})
    conn.commit()
    return []

@app.route("/addQuestion/<question>/<learningobject>/<authorobject>", methods=['POST'])
def addQuestion(question, learningobject, authorobject):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    last_id = cursor.execute(f"SELECT MAX(id) FROM vragen").fetchone()
    last_id = last_id[0] + 1
    rows = cursor.execute(
        f"INSERT INTO vragen (id, vraag, leerdoel, auteur) VALUES (:id, :text, :learningobject, :authorobject);",
        {"id": last_id, "text": "" + question + "", "learningobject": learningobject, "authorobject": authorobject})
    conn.commit()
    return []

@app.route("/getResults/<textInput>", methods=['GET'])
def getResults(textInput):
    query = '%' + textInput + '%'
    cursor = sqlite3.connect(DATABASE_FILE).cursor()
    rows = cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vragen.vraag, auteurs.voornaam FROM vragen, leerdoelen, auteurs WHERE leerdoelen.id == vragen.leerdoel AND vragen.auteur == auteurs.id AND vragen.leerdoel <= 7 AND vraag LIKE ? LIMIT 8",
                          (query,)).fetchall()
    return rows

@app.route("/getResultsId/<textInput>", methods=['GET'])
def getResultsId(textInput):
    query = textInput
    cursor = sqlite3.connect(DATABASE_FILE).cursor()
    rows = cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vragen.vraag, auteurs.voornaam FROM vragen, leerdoelen, auteurs WHERE leerdoelen.id == vragen.leerdoel AND vragen.auteur == auteurs.id AND vragen.leerdoel <= 7 AND vragen.id = ? LIMIT 8",
                          (query,)).fetchall()
    return rows
    

@app.route("/showMoreResults/<showMoreBtnValue>", methods=['GET'])
def showMoreResults(showMoreBtnValue):
    query = showMoreBtnValue
    cursor = sqlite3.connect(DATABASE_FILE).cursor()
    rows = cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vragen.vraag, auteurs.voornaam FROM vragen, leerdoelen, auteurs WHERE leerdoelen.id == vragen.leerdoel AND vragen.auteur == auteurs.id AND vragen.leerdoel <= 7 LIMIT ?",
                          (query,)).fetchall()
    return rows

@app.route("/getModalResults/<rowId>", methods=['GET'])
def getResultsModal(rowId):
    query = rowId
    cursor = sqlite3.connect(DATABASE_FILE).cursor()
    row = cursor.execute(f"SELECT * FROM vragen WHERE id = ?",
                         (query,)).fetchall()
    return row

@app.route("/getModalAuthorResults/<rowId>", methods=['GET'])
def getResultsModalAuthor(rowId):
    query = rowId
    cursor = sqlite3.connect(DATABASE_FILE).cursor()
    row = cursor.execute(f"SELECT * FROM auteurs WHERE id = ?",
                         (query,)).fetchall()
    return row

@app.route("/edithInfo/<id>/<question>/<learningobject>/<authorobject>", methods=['POST'])
def editModalInfo(id, question, learningobject, authorobject):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    rows = cursor.execute(
        f"UPDATE vragen SET vraag = :text, leerdoel = :learningobject, auteur = :authorobject WHERE id = :id",
        {"text": "" + question + "", "learningobject": learningobject, "id": id, "authorobject": authorobject})
    conn.commit()
    return []
    
# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name):
    if table_name == 'leerdoelen':
        rows, column_names = dbm.get_learningobject_content()
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name, name=current_user.name
        )

    elif table_name == 'auteurs':
        rows, column_names = dbm.get_authors_content()
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name, name=current_user.name
        )


# Auth routes

# Naar de login view
@app.route('/login')
def login():
    return render_template(
        "login.html"
    )


# Het verweken van de login request
@app.route('/loginReq', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # Controleert of de user bestaat
    if not user or not check_password_hash(user.password, password):
        flash('Controleer uw inloggegevens en probeer het opnieuw.')
        return redirect(url_for('login'))  # Als de user niet bestaat gaat hij naar de login pagina

    # Als alles goed gaat logt hij de user in
    login_user(user)

    return redirect(url_for('index'))

# Naar sign up view
@app.route('/signup')
def signup():
    return render_template(
        "signup.html"
    )

# Het verwerken van de sign up request
@app.route('/signupReq', methods=['POST'])
def signup_post():
    # haalt de data van de request op
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()  # controlleert of de email al bestaat

    if user:  # als user een waarde heeft word hij terug gestuurd met deze message
        flash('Email is al in gebruik')
        return redirect(url_for('signup'))

    if name == '':
        flash('Vul alle velden in')
        return redirect(url_for('signup'))

    # maakt een nieuwe user aan met een gehased password.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # voegt user toe aan db
    db.session.add(new_user)
    db.session.commit()

    # verstuurd de user naar de login page
    return redirect(url_for('login'))

# Het uitloggen van de user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
