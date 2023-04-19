from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/show/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('show.html', suser = User.get_one(session['user_id']), recipe = Recipe.get_one_with_users_id(id))

@app.route('/add_recipe')
def add_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_recipe.html', suser = User.get_one(session['user_id']))




@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/add_recipe')
    
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': request.form['under30'],
        'created_at': request.form['created_at'],
        'user_id': request.form['user_id']
    }
    print(data)
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit.html', suser = User.get_one(session['user_id']), recipe = Recipe.get_one_with_users_id(id))

@app.route('/update', methods = ['POST'])
def update():
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{request.form["recipe.id"]}')
    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    Recipe.delete(id)
    return redirect('/dashboard')