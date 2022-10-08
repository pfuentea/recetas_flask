from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user_models import User
from flask_app.models.recipe_models import Recipes

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('log_reg.html')

@app.route('/registrar_usuario', methods=['POST'])
def registro():

    if not User.validacion(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    usuario_id = User.ingreso(data)
    # guardamos el id del usuario registrado en la sesion para empezar a darle seguimiento
    session ['usuario_id'] = usuario_id
    return redirect ('/welcome')

@app.route('/login', methods=['POST'])
def login():
    usuario_loggeado = User.validar_login(request.form)
    print(usuario_loggeado, 'QUE CONTIENES ESTO_')
    if not usuario_loggeado[0]:
        return redirect("/")
    # guardamos el id del usuario registrado en la sesion para empezar a darle seguimiento
    session['usuario_id'] = usuario_loggeado[1].id
    return redirect('/welcome')


@app.route('/welcome')
def welcome():
    if 'usuario_id' not in session:
        return redirect("/")

    data = {
        'id':session['usuario_id']
    }

    print(data)
    usuario_ingreso = User.obtener_un_usuario(data)
    #todas_recetas = Recipes.todas_recetas()
    todas_recetas_con_usuarios = Recipes.recetas_con_usuarios()
    return render_template('datos.html', usuario_ingreso=usuario_ingreso, todas_recetas_con_usuarios=todas_recetas_con_usuarios)

@app.route("/logout")
def limpiar_session():
    session.clear()
    return redirect('/')