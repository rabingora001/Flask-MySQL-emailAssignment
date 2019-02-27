from flask import Flask, render_template,redirect, request,flash,session
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/process", methods=['post'])
def process():
    errors=False
  
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!", 'email')
        errors=True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", 'email') 
        errors=True   
    elif len(request.form['email']) <= 3:
        flash("email must be 3+ characters", 'namemail')
        errors=True
    if errors==True:
        return redirect("/")
    else:
        mysql = connectToMySQL('emailVal')
        query = "INSERT INTO user_email (email) VALUES (%(email)s);"
        data = { "email" : request.form['email'] }
        mysql.query_db(query, data)
        
        return redirect("/success")


    

@app.route("/success")
def success():
    mysql = connectToMySQL('emailVal')
    query= "select * from user_email"
    email=mysql.query_db(query)     
    return render_template("success.html",allemails=email)


    





if __name__=="__main__":
    app.run(debug=True)
