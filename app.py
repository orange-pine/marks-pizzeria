from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from config import Config
from models import db, Pizzas


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

PIZZA_BASE_PRICE = 7.00

####################################
# routes
####################################


@app.route('/',  methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route('/menu',  methods=["GET","POST"])
def menu():
    return render_template("menu.html", pizzas = get_pizzas(None))

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

def get_pizzas(filter):
    pizza_dics = []
    pizzas = Pizzas.query.filter_by(name=filter).all()

    for pizza in pizzas:
        pizza_dics.append({
            'id': pizza.id,
            'name': pizza.name,
            'description': get_description(0,pizza.id),
            'price': calculate_base_price(pizza.get_ingredient_price()),
            'image': get_image(0,pizza.id) or '/static/images/default-pizza.jpg',


        })



    return pizza_dics

def get_image(type, id):
    return '/static/images/default.jpg'

def get_description(type, id):
    return ""

def calculate_base_price(ingredient_list):
    return round(PIZZA_BASE_PRICE + sum(ingredient_list),2)




def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True, port=6009)