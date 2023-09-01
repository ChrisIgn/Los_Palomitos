from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session, flash
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
#from config import config
#from flask_wtf.csrf import CSRFProtect
#from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__,template_folder='templates')

#Coneccion MYSQL 
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='chris'
app.config['MYSQL_PASSWORD'] ='123#Hola@'
app.config['MYSQL_DB'] ='flaskcontacts'
mysql = MySQL(app)

#Configuraciones
app.secret_key = 'mysecretkey'

#Login index de la pagina web
@app.route('/')
def home():
    return render_template('index.html')

#cuentas admin
@app.route('/admin')
def admin():
    return render_template('admin.html')

#Funcion de login
@app.route('/acceso-login', methods= ["GET","POST"])
def login():
   
    if request.method == 'POST' and 'txtUsuario' in request.form and 'txtPassword' in request.form:
       
        _usuario = request.form['txtUsuario']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE usuario = %s AND password = %s', (_usuario, _password,))
        account = cur.fetchone()
        if account:

            session['logueado'] = True
            session['id'] = account[0] 

            return redirect(url_for('contacts_info'))
            #return render_template("admin.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")

#Informacion de contactos donde se realizan modificaciones
@app.route('/contacts_info')
def contacts_info():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('contact_info.html', contacts = data)


#Definimos la ruta para poder agregar contactos u alumnos?
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('Nombre de Alumno añadido')
        return redirect(url_for('contacts_info'))

#Definimios la ruta para poder realizar la modificacion de algun contacto
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('Edit_contact.html', contact = data[0])


#Ruta para poder realizar una eliminacion de un contacto u alumno en nuestro caso?
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Alumno Removido')
    return redirect(url_for('contacts_info'))

@app.route('/update/<id>', methods= ['POST'])
def update_conctat(id):
    if request.method == 'POST': 
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']  
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Datos de alumno modificados')
        return redirect(url_for('contacts_info'))


if __name__ == '__main__':
#    app.config.from_object(config['development'])
    app.run(host="45.236.129.34",port = 5173, debug = True)
