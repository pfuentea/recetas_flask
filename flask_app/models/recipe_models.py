from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models.user_models import User

class Recipes:
    db='recetas_usuarios'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under = data['under']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data["user_id"]
        self.usuario = []

    @classmethod
    def crear_receta(cls, data):
        consulta = """ INSERT INTO recipes (name, description, date_made, under,  instruction, user_id )
                        VALUES( %(name)s, %(description)s, %(date_made)s, %(under)s, %(instruction)s, %(usuario_id)s);"""
        resultado = connectToMySQL('recetas_usuarios').query_db(consulta, data)
        return resultado
    
    @classmethod
    def todas_recetas(cls):
        consulta = "SELECT * FROM recipes;"
        resultado = connectToMySQL(cls.db).query_db(consulta)
        todas_las_recetas = []
        for receta in resultado:
            todas_las_recetas.append(cls(receta))
        return todas_las_recetas   
    
    @classmethod
    def recetas_con_usuarios(cls):
        consulta = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        resultado = connectToMySQL(cls.db).query_db(consulta)
        todas_las_recetas_con_usuarios = []
        for receta in resultado:
            objeto_receta = cls(receta)
            objeto_receta.usuario.append(User(receta))
            todas_las_recetas_con_usuarios.append(objeto_receta)
        return todas_las_recetas_con_usuarios 

    @classmethod 
    def receta_by_id(cls,data):
        consulta = "SELECT * FROM recipes WHERE id= %(id)s;"
        resultado = connectToMySQL(cls.db).query_db(consulta, data)
        return cls(resultado[0])

    @classmethod 
    def update_receta(cls,data): 
        consulta = "UPDATE recipes SET name=%(name)s, description= %(description)s,  date_made=%(date_made)s, under= %(under)s,  instruction=%(instruction)s  WHERE id= %(receta_id)s;"
        resultado = connectToMySQL(cls.db).query_db(consulta, data)
        
    @classmethod
    def delete_receta(cls,data):
        consulta = "DELETE from recipes WHERE id= %(receta_id)s;"
        resultado = connectToMySQL(cls.db).query_db(consulta, data) 