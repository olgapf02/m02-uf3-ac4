# -*- coding: utf-8 -*-
"""
Created on February 2023

@author: Albert ETPX
"""
# Importación de módulos externos
import mysql.connector
from flask import Flask,render_template,request;

# Funciones de backend #############################################################################

# connectBD: conecta a la base de datos users en MySQL
def connectBD():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "gaol1920",
        database = "users"
    )
    return db

# initBD: crea una tabla en la BD users, con un registro, si está vacía
def initBD():
    bd=connectBD()
    cursor=bd.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS users;")
    # Operación de creación de la tabla users (si no existe en BD)
    query="CREATE TABLE IF NOT EXISTS users(\
            user varchar(30) primary key,\
            password varchar(30),\
            name varchar(30), \
            surname1 varchar(30), \
            surname2 varchar(30), \
            age integer, \
            genre enum('H','D','NS/NC')); "
    cursor.execute(query)
            
    # Operación de inicialización de la tabla users (si está vacía)
    query="SELECT count(*) FROM users;"
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    if(count == 0):
        query = "INSERT INTO users \
            VALUES('user01','admin','Ramón','Sigüenza','López',35,'H');"
        cursor.execute(query)

    bd.commit()
    bd.close()
    return

# checkUser: comprueba si el par usuario-contraseña existe en la BD
def checkUser(user,password):
    bd=connectBD()
    cursor=bd.cursor()

    query=f"SELECT user,name,surname1,surname2,age,genre FROM users WHERE user=%s \
            AND password=%s"
    param= (user,password)
    print(query)
    cursor.execute(query,param)
    userData = cursor.fetchall()
    bd.close()
    
    if userData == []:
        return False
    else:
        return userData[0]

# cresteUser: crea un nuevo usuario en la BD
def createUser(user,password,name,surname1,surname2,age,genre):
    
    return

# Secuencia principal: configuración de la aplicación web ##########################################
# Instanciación de la aplicación web Flask
app = Flask(__name__)

# Declaración de rutas de la aplicación web
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    initBD()
    return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/results",methods=('GET', 'POST'))
def results():
    if request.method == ('POST'):
        formData = request.form
        user=formData['usuario']
        password=formData['contrasena']
        userData = checkUser(user,password)

        if userData == False:
            return render_template("results.html",login=False)
        else:
            return render_template("results.html",login=True,userData=userData)
        

@app.route('/newUser', methods=['POST'])
def register():
    # Obté les dades del formulari
    username = request.form['username']
    password = request.form['password']
    nom = request.form['nom']
    cognom1 = request.form['cognom1']
    cognom2 = request.form['cognom2']
    edat = request.form['edat']
    salari = request.form['salari']


# Funció per a crear un nou usuari a la base de dades
def createUser(username, password, nom, cognom1, cognom2, edat, salari):
    # Connecta amb la base de dades
    conn = bd=connectBD()
    # Crea un cursor per a executar les sentències SQL
    cursor=bd.cursor()
    # Sentència SQL per a inserir un nou usuari a la base de dades
    query = """INSERT INTO users (username, password, nom, cognom1, cognom2, edat, salari)
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    # Valors per a la sentència parametritzada
    values = (username, password, nom, cognom1, cognom2, edat, salari)
    # Executa la sentència SQL amb els valors
    cursor.execute(query, values)
    # Confirma els canvis a la base de dades
    conn.commit()
    # Tanca la connexió i el cursor
    cursor.close()
    conn.close()
        
# Configuración y arranque de la aplicación web
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='localhost', port=5000, debug=True)
