from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)





@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sign_up', methods = ['POST'])
def sign_up():
    if not User.validate_sign_up(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['pass'])
    # print(pw_hash)
    data = {
        'first_name':request.form['fname'],
        'last_name':request.form['lname'],
        'email':request.form['email'],
        'password':pw_hash
    }
    user_id = User.save(data)
    
    session['user_id'] = user_id

    return redirect('/dashboard')


@app.route('/login', methods = ['POST'])
def login():
    logged_in_user = User.validate_login(request.form)
    if logged_in_user:
        session['user_id'] = logged_in_user.id
        return redirect("/dashboard")
    else:
        return redirect('/')




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('dashboard.html', suser = User.get_one(session['user_id']), recipes = Recipe.get_all_with_users())


@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')