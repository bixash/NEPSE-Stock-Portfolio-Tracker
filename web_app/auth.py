from flask import Blueprint, render_template, url_for, request, session, redirect
from .db import cur, con

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])

def login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      err_msg = []

      if not email:
         err_msg.append("Email shouldn't be empty!") 

      if not password:
         err_msg.append("Password shouldn't be empty!")


      if not err_msg:
         try:
            cur.execute("SELECT id, username FROM `User` where email= ? and password = ?", (email, password))
            result = cur.fetchone()


            user_id = result[0]
            username = result[1]

            if result:
               session['user_id'] = user_id
               session['username'] = username
         
            return redirect(url_for('views.dashboard'))
         except Exception as e:
            err_msg.append(e)
            return render_template("login.html", msg = err_msg)
      else: 
         err_msg = "Username or password invalid!!"
         return render_template("login.html", msg = err_msg)
   return render_template("login.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      username = request.form.get("username", False)

      err_msg = []
      if not email:
         err_msg.append("Email shouldn't be empty!") 
      
      if not password:
         err_msg.append("Password shouldn't be empty!")
      
      if not username:
        err_msg.append("Username shouldn't be empty!")
         
      if not err_msg:
         try:
            cur.execute("INSERT INTO user(username, email, password) values(?,?,?)",(username, email, password, ))
            con.commit()
            return render_template("login.html", msg = "Account created!")
         except Exception as e:
            err_msg.append(e)
            return render_template("signup.html", err = err_msg)
      else: 
         return render_template("signup.html", err = err_msg)

   return render_template("signup.html")

@auth.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('user_id', None)

   return redirect(url_for("views.home"))