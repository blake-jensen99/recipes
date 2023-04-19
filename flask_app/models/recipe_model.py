from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash, request

from flask_app import DB, app



from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data["name"]
        self.under30 = data['under30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, under30, description, instructions, created_at, user_id) VALUES ( %(name)s, %(under30)s, %(description)s, %(instructions)s, %(created_at)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, created_at = %(created_at)s WHERE recipes.id = %(recipe.id)s'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        data = {'id': id}
        query = 'DELETE FROM recipes WHERE recipes.id = %(id)s'
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_all_with_users(cls):
        from flask_app.models.user_model import User
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        recipes = []
        if results:
            for row in results:
                recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                row = User(user_data)
                recipe.creator = row
                recipes.append(recipe)
        return recipes

    @classmethod
    def get_one_with_users_id(cls, id):
        from flask_app.models.user_model import User
        data = {'id': id}
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        row = results[0]
        
        recipe = cls(row)
        user_data = {
            **row,
            'id': row['users.id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        single = User(user_data)
        
        recipe.creator = single
        return recipe
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(request.form['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False

        if len(request.form['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        
        if len(request.form['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False

        if request.form['created_at'] == '':
            flash('Date must be suplied.')
            is_valid = False

        return is_valid