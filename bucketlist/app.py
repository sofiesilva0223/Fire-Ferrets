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
  'password': 'Tintinnabulation321!',
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
    #if session.get('user'):
    return render_template('userHome.html')
    #else:
        #return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        if session.get('user'):
            
            _id = request.form['id']
            _user = session.get('user')
    
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetWishById',(_id,_user))
            result = cursor.fetchall()

            wish = []
            wish.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2]})

            return json.dumps(wish)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
        
@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()

            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)

            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')

            cursor.callproc('sp_addWish',(_title,_description,_user))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')

        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

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
            return json.dumps({'httml':'<span>Enter the required fields</span>'})
    finally:
        cur.close()
        conn.close()

            


if __name__ == "__main__":
    app.run()
