from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from config import Config
from models import db



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()




@app.route('/',  methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route('/menu',  methods=["GET","POST"])
def menu():
    return render_template("menu.html")

@app.route('/checkout',  methods=["GET","POST"])
def checkout():
    return render_template("checkout.html")



@app.route('/admin',  methods=["GET","POST"])
def admin():
    if not session.get('admin'):
        return redirect('/admin/login')


    return render_template("index.html")


@app.route('/logout', methods=["GET","POST"])
def logout():
    session.pop('admin', None)
    session.pop('username', None)
    session.pop('password', None)

    return redirect(url_for('index'))


@app.route('/admin/login', methods=["GET","POST"])
def admin_login():
    return render_template("login_admin.html")

@app.route("/admin/login/submit", methods=["GET","POST"])
def admin_login_submit():

    session["username"] = request.form['username']
    session["password"] = encrypt(request.form['password'])
    session['admin'] = True

    print(session)

    return redirect("/")




def encrypt(password):
    return "stfu"


if __name__ == '__main__':
    app.run(debug=True, port=6009)