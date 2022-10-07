
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')

class User: 
    base_datos="recetas_usuarios"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def ingreso(cls,data):
        solicitud = """INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW()); """
        return connectToMySQL(cls.base_datos).query_db(solicitud,data)

    @classmethod
    def obtener_email(cls, data):
        solicitud = "SELECT * FROM users WHERE email = %(email_1)s;"
        resultado = connectToMySQL(cls.base_datos).query_db(solicitud, data)
        #validar si el resultado contiene algo
        if len(resultado) < 1:
            return False
        return cls(resultado[0])
    
    @classmethod
    def obtener_un_usuario(cls, data):
        solicitud = "SELECT * FROM users WHERE id = %(id)s;"
        resultado = connectToMySQL(cls.base_datos).query_db(solicitud, data)
        return cls(resultado[0])

    @staticmethod
    def validacion(user):
        is_valid = True # asumimos que esto es true
        if len(user['first_name']) < 3:
            flash("Name must be at least 3 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        if len(user['password']) < 6:
            flash("password must be at least 6 characters.", 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords do not match!", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validar_login(formulario_login):
        is_valid = True
        obtener_usuario = User.obtener_email(formulario_login)
        if obtener_usuario == False:
            flash("Correo electronico no existe!", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(obtener_usuario.password, formulario_login['password_1']):
        # si obtenemos False después de verificar la contraseña
            flash("Invalid Email/Password", "login")
            is_valid=False
        return is_valid, obtener_usuario


