from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe_models import  Recipes


@app.route('/crear_receta')
def formulario_receta():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('crear_receta.html')

@app.route('/crear_receta', methods=['POST'])
def crear_receta():
    receta_id=Recipes.crear_receta(request.form)
    return redirect("/welcome")
