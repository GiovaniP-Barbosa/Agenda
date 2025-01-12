from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Usando SQLite
app.secret_key = 'sua_chave_secreta'
db = SQLAlchemy(app)

# Definindo o modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Definindo o usuário administrador e senha (hash)
ADMIN_USER = "Giovani Pereira Barbosa"
ADMIN_PASS = generate_password_hash("Giovani Pereira Barbosa")  # Senha com hash

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        # Verificando se o usuário e senha estão corretos
        if usuario == ADMIN_USER and check_password_hash(ADMIN_PASS, senha):
            return redirect(url_for("dashboard"))
        else:
            flash("Usuário ou senha incorretos!", "danger")
            return render_template("login.html")

    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Criando um novo usuário e salvando no banco
        new_user = User(nome=nome, email=email, senha=generate_password_hash(senha))
        db.session.add(new_user)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    db.create_all()  # Criar tabelas no banco de dados
    app.run(debug=True)

