from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash, request
from flask_app.models.recipe_model import Recipe

from flask_app import DB, app

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUE ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NoW() );"
        return connectToMySQL(DB).query_db(query, data)
        

    @classmethod
    def get_one(cls, id):
            query = "SELECT * FROM users WHERE id = %(id)s"
            data = {'id':id}
            results = connectToMySQL(DB).query_db(query, data)
            return cls(results[0])


    @classmethod
    def get_by_email(cls,data):
        data = {'email': data}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    

    

    @staticmethod
    def validate_sign_up(data):
        is_valid = True

        if len(request.form['fname']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False

        if len(request.form['lname']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False

        if not EMAIL_REGEX.match(request.form['email']):
            is_valid = False
            flash("Email is invalid.")
        
        if len(request.form['pass']) < 3:
            flash("Password must be at least 3 characters.")
            is_valid = False

        if request.form['pass'] != request.form['con_pass']:
            flash('Passwords do not match.')
            is_valid = False

        return is_valid
    


    @classmethod
    def validate_login(cls, form):
        found_user = cls.get_by_email(form['lemail'])
        
        if found_user:
            if bcrypt.check_password_hash(found_user.password, form['lpass']):
                return found_user
            else:
                flash('Invalid Login')
                return False
        else:
            flash('Invalid Login')
            return False

        return is_valid
    
    