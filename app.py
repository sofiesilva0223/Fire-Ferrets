from flask import Flask, render_template, json, request,redirect,session,jsonify
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
#mysql = MySQL(app)
app.secret_key = 'why would I tell you my secret key?'

config = {
  'user': 'root',
  'port': '3322',
  'password': 'ScottPilgrim1!',
  'host': 'localhost',
  'database': 'bucketlist',
  'raise_on_warnings': True
}

# MySQL configurations
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'Tintinnabulation321!'
#app.config['MYSQL_DB'] = 'bucketlist'
#app.config['MYSQL_HOST'] = 'localhost'
#app.debug = True
#mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')



@app.route('/validateLogin',methods=['POST'])
def validateLogin():

    conn = MySQLConnection(**config)
    cur = MySQLCursor(conn)

    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
                
        # connect to mysql

        cur.callproc('sp_validateLogin',(_username,))
        data = cur.fetchall()
        print(data)

        #if len(data) > 0:
        session['user'] = data[0][0]          
        return redirect('/userHome')
        #else:
        #    return render_template('error.html',error = 'Wrong Email address or Password.')
            

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cur.close()
        conn.close()


@app.route('/signUp',methods=['POST','GET'])
def signUp():

    conn = MySQLConnection(**config)
    cur = MySQLCursor(conn)

    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            #_hashed_password = generate_password_hash(_password)
            cur.callproc('sp_createUser',(_name,_email,_password))

            data = cur.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else: 
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    finally:
        cur.close()
        conn.close()

@app.route('/writeWish',methods=['POST','GET'])
def writeWish():

    conn = MySQLConnection(**config)
    cur = MySQLCursor(conn)

    try:
        _name = request.form['inputWishname']
        _info = request.form['inputInfo']


        # validate the received values
        if _name and _info:

            #_hashed_password = generate_password_hash(_password)
            cur.callproc('sp_createWish1',(_name,_info))

            data = cur.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'Wish created successfully !'})
            else: 
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    app.run()