from flask import Flask, render_template, json, request,redirect,session,jsonify
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import uuid
import os

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

config = {
  'user': 'root',
  'password': 'Tintinnabulation321!',
  'host': 'localhost',
  'database': 'bucketlist',
  'raise_on_warnings': True
}

app.debug = True

#Default Setting
pageLimit = 2

app.config['UPLOAD_FOLDER'] = 'C:/Users/Edin/Desktop/Fall 2021/CMPE131/FireFerrets/Fire-Ferrets/bucketlist/static/Uploads'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})

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

@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')

            conn = MySQLConnection(**config)
            cur = conn.cursor(cursor_class=MySQLCursor)
            cur.callproc('sp_deleteWish',(_id,_user))
            result = cur.fetchall()

            if len(result) == 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cur.close()
        conn.close()

@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        if session.get('user'):
            
            _id = request.form['id']
            _user = session.get('user')
    
            conn = MySQLConnection(**config)
            cur = conn.cursor(cursor_class=MySQLCursor)
            #cur.callproc('sp_GetWishById',(_id,_user))
            select_stmt = "select wish_id,wish_title,wish_description,wish_file_path,wish_private,wish_accomplished from tbl_wish where wish_id = %(_id)s and wish_user_id = %(_user)s"
            cur.execute(select_stmt, {'_id':_id, '_user':_user})
            result = cur.fetchall()

            wish = []
            wish.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2],'Private':result[0][4],'Done':result[0][5]})

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
            #_limit = pageLimit
            #_offset = request.form['offset']
            #print(_offset)
            #_total_records = 0

            con = MySQLConnection(**config)
            cur = con.cursor(dictionary=True, cursor_class=MySQLCursor)
            #cur.callproc('sp_GetWishByUser',(_user,))

            
            select_stmt = "select * from tbl_wish where wish_user_id = %(_user)s"   
            #select count(*) into %(_total_records)s from tbl_wish where wish_user_id = %(_user)s; 
            #SET @t1 = CONCAT( 'select * from tbl_wish where wish_user_id = ',%(_user)s,' order by wish_date desc limit ',%(_limit)s,' offset ',%(_offset)s);
	        #PREPARE stmt FROM @t1;
	        #EXECUTE stmt;
	        #DEALLOCATE PREPARE stmt1;
            #"""

            cur.execute(select_stmt, {'_user': _user})
            
            wishes = cur.fetchall()
            #cur.close()

            #ur = con.cursor(dictionary=True, cursor_class=MySQLCursor)

            #cur.execute('SELECT @_sp_GetWishByUser_3')

            #outParam = cur.fetchall()

            #response = []
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)
            #response.append(wishes_dict)
            #response.append({'total':outParam[0][0]}) 

            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        conn = MySQLConnection(**config)
        cur = conn.cursor(cursor_class=MySQLCursor)

        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')

            if request.form.get('filePath') is None:
                _filePath = ''
            else:
                _filePath = request.form.get('filePath')
            if request.form.get('private') is None:
                _private = 0
            else:
                _private = 1
            if request.form.get('done') is None:
                _done = 0
            else:
                _done = 1

            cur.callproc('sp_addWish',(_title,_description,_user, _filePath, _private, _done))
            data = cur.fetchall()

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
        cur.close()
        conn.close()

@app.route('/updateWish', methods=['POST'])
def updateWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _wish_id = request.form['id']

            

            conn = MySQLConnection(**config)
            cur = conn.cursor(cursor_class=MySQLCursor)
            cur.callproc('sp_updateWish',(_title,_description,_wish_id,_user))
            data = cur.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cur.close()
        conn.close()

@app.route('/validateLogin',methods=['POST'])
def validateLogin():

    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        conn = MySQLConnection(**config)
        cur = conn.cursor(named_tuple=True, buffered=True, dictionary=True, cursor_class=MySQLCursor)

        #cur.callproc('sp_validateLogin', (_username,))
        select_stmt = "SELECT * FROM tbl_user WHERE user_username = %(_username)s"
        cur.execute(select_stmt, {'_username': _username})
        data = cur.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]          
                return redirect('/userHome')
            else:
                return render_template('error.html', error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
        
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cur.close()
        conn.close()


@app.route('/signUp',methods=['POST','GET'])
def signUp():

    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            conn = MySQLConnection(**config)
            cur = MySQLCursor(conn)
            _hashed_password = generate_password_hash(_password)
            cur.callproc('sp_createUser',(_name,_email,_hashed_password))

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
