from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from models import Base, Pizza  # import your SQLAlchemy 2.0 models
from config import Config

# ----------------------------------------
# Flask setup
# ----------------------------------------

app = Flask(__name__)
app.config.from_object(Config)


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=False, future=True)
Base.metadata.create_all(engine)

# Thread-safe session factory
session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
db_session = scoped_session(session_factory)
session = Session(engine)

PIZZA_BASE_PRICE = 7.00

# ----------------------------------------
# Helper functions
# ----------------------------------------



def get_image(type, id):
    return "/static/images/default.jpg"


def get_description(type, id):
    return ""


def calculate_base_price(ingredient_list):
    return round(PIZZA_BASE_PRICE + sum(ingredient_list), 2)


def get_pizzas(filter_name=None):
    pizza_dicts = []

    with db_session() as session:
        stmt = select(Pizza)
        if filter_name:
            stmt = stmt.where(Pizza.name == filter_name)

        pizzas = session.scalars(stmt).all()

        for pizza in pizzas:
            pizza_dicts.append({
                "id": pizza.id,
                "name": pizza.name,
                # "description": get_description(0, pizza.id),
                "price": pizza.price,
                # "image": get_image(0, pizza.id) or "/static/images/default-pizza.jpg",
            })

    return pizza_dicts


# ----------------------------------------
# Routes
# ----------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")


@app.route("/menu", methods=["GET", "POST"])
def menu():
    pizza_dicts = []
    with engine.connect() as conn:
        for pizza in session.scalars(select(Pizza)):
            pizza_dicts.append({
                "id": pizza.id,
                "name": pizza.name,
                # "description": get_description(0, pizza.id),
                "ingredients" : pizza.ingredients,
                "price": pizza.price,
                # "image": get_image(0, pizza.id) or "/static/images/default-pizza.jpg",
            })
    print(pizza_dicts)
    return render_template("menu.html", pizzas=pizza_dicts)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    return render_template("checkout.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/admin/login")
    return render_template("index.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("admin", None)
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("index"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    return render_template("login_admin.html")


@app.route("/admin/login/submit", methods=["GET", "POST"])
def admin_login_submit():
    session["username"] = request.form["username"]
    session["password"] = encrypt(request.form["password"])
    session["admin"] = True
    return redirect("/")


# ----------------------------------------
# Database Initialization
# ----------------------------------------

def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
        print("✅ Database tables created successfully!")


if __name__ == "__main__":
    app.run(debug=True, port=6009)

