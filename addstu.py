from flask import request, render_template, redirect, url_for, Flask,flash,session
from studentr.models import Studentdetails
from passlib.hash import sha256_crypt
from functools import wraps

import sqlite3
import os


studentr = Flask(__name__)
studentr.secret_key=os.urandom(24)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
            
        else:
            flash("Error : You need to login first")
            return redirect(url_for('login'))

    return wrap






@studentr.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        con= sqlite3.connect('studentrec.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        row = cur.execute('select * from users where username = ?',(request.form['username'],))
        
        data = row.fetchone()[2]
        if data == None:
            flash('you must fill your password')
        
        if sha256_crypt.verify(request.form['password'],data):
            session['logged_in'] = True
            session['username'] = request.form['username']
            
            flash('you are now logged')
            return redirect(url_for('addrec'))
        else:
            flash('invalid Cred , try again')
            
    return render_template('login.html')
            
        
    
    
@studentr.route('/registor',methods=['GET','POST'])

def registor():
    
    
    if request.method == 'POST' :
        username = request.form['username']
        password = sha256_crypt.encrypt((str(request.form['password'])))

        with sqlite3.connect('studentrec.db') as con:
            cur = con.cursor()
    
            cur.execute('SELECT * FROM users WHERE username = ?', (username,))
            if cur.fetchone() is not None:
                flash('Error: username is already taken')
                return redirect(url_for('registor'))
            else:
                cur.execute("INSERT into users(username,password) VALUES(?,?)", (username, password))
                con.commit()
                flash('user created: Kindly click on login link')
                return redirect(url_for('registor'))
            
    elif request.method == 'GET':
        return render_template("registor.html")

    else:
        flash('Error: All fields are required')

    return render_template("registor.html")
    
    
    


@studentr.route('/addrec', methods=["GET", "POST"])
@login_required
def addrec():
    form = Studentdetails(request.form)

    if request.method == 'POST' and form.validate():
    
        firstname = form.fname.data
        lastname = form.lname.data
        id = form.stid.data
            
        
        with sqlite3.connect('student.db') as con:
             cur=con.cursor()

             cur.execute('SELECT * FROM students WHERE stid = ?', (id,))
             if cur.fetchone() is not None:
                     flash('Error: id is already taken')
                     return redirect(url_for('addrec'))
             else:
                 cur.execute("INSERT into students(fname,lname,stid) VALUES(?,?,?)" ,(firstname,lastname,id))
                 con.commit()
                 flash('posted')
                 return redirect(url_for('addrec'))
        
        
    elif request.method == 'GET':
        return render_template("stu.html", form=form)
        
    else:
        flash('Error: All fields are required')

    
    return render_template("stu.html",form = form)
            




@studentr.route('/list')
@login_required
def list():
    con = sqlite3.connect('student.db')
    con.row_factory=sqlite3.Row
    cur = con.execute('SELECT stid,fname,lname from students')
    
    row = cur.fetchall()
    return render_template("list.html", row=row)


@studentr.route('/delete', methods=['GET','POST'])
@login_required
def delete():
    
    
    if request.method == 'POST':
        id = request.form['studentid']
        con = sqlite3.connect('student.db')
        cur = con.cursor()
        cur.execute('select * from students where stid = ?', (id,))
        if cur.fetchone() is None:
            flash('Error: id not present')
            return redirect(url_for('delete'))
        else:
            cur.execute('delete from students where stid = ?', (id,))
            con.commit()
            flash('Id has been deleted')
            return redirect(url_for('delete'))
        
    return render_template('del.html')

@studentr.route('/search', methods=['GET','POST'])
@login_required
def search():
    con = sqlite3.connect('student.db')
    cur = con.cursor()
    con.row_factory = sqlite3.Row
    
    cur.execute('select stid from students')
    rows = cur.fetchall()
    return render_template('ser.html', row=rows)
        
    
    
    

    
    

if __name__ == "__main__":
    studentr.run(debug=True)