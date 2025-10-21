from flask import Flask, request, jsonify, render_template, session as fsession, redirect, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from models import Base, Pizza, Customer, Order  # import your SQLAlchemy 2.0 models
from config import Config
from contextlib import contextmanager
import utils

# ----------------------------------------
# Flask setup
# ----------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)

# Thread-safe session factory
# session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
# db_session = scoped_session(session_factory)
session = Session(engine)



# ----------------------------------------
# Helper functions
# ----------------------------------------



# def get_image(type, id):
#     return "/static/images/default.jpg"


# def get_description(type, id):
#     return ""





def get_pizzas(filter_name=None):
    pizza_dicts = []
    for pizza in session.scalars(select(Pizza)):
        pizza_dicts.append({
            "id": pizza.id,
            "name": pizza.name,
            # "description": get_description(0, pizza.id),
            "ingredients" : pizza.ingredients,
            "price": utils.calculate_pizza_price(pizza.price),
            # "image": get_image(0, pizza.id) or "/static/images/default-pizza.jpg",
        })

    return pizza_dicts
#
def get_total_price(item_dic):
    total_price = 0

    for item in item_dic:
        total_price += item["price"]

    return total_price


def convert_postcode(postcode):
    pc = 0
    pc += int(postcode[0:3]) * 10000
    pc += int(postcode[4]) * 100
    pc += int(postcode[5])
    return pc
# ----------------------------------------
# Transaction manager
# ----------------------------------------

@contextmanager
def transaction():
    try:
        yield db_session
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.remove()




# ----------------------------------------
# Routes
# ----------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/menu", methods=["GET", "POST"])
def menu():
    return render_template("menu.html", pizzas=get_pizzas())

@app.route("/menu/add_to_cart", methods=["GET", "POST"])
def add_to_cart():
    added_item = {
        "id" : request.form.get("item_id"),
        "type" : request.form.get("item_type"),
        "name" : request.form.get("item_name"),
        "price" : float(request.form.get("item_price"))
    }
    try:
        fsession["cart"].append(added_item)
    except:
        fsession["cart"] = [added_item]
    fsession.modified = True

    return redirect(url_for("menu"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():


    item_dic = fsession["cart"]
    return render_template("checkout.html", cart_items=item_dic, total = get_total_price(item_dic))

@app.route("/checkout/remove_from_cart", methods=["GET", "POST"])
def remove_from_cart():
    deleted_item = request.form.get("item_id")
    fsession["cart"].remove(deleted_item)
    return redirect(url_for("checkout"))

@app.route("/checkout/place_order", methods=["GET", "POST"])
def place_order():

    #try:
        with transaction() as t:
            print(request.form.get("postcode"))
            customer = Customer(
                id = db_session.scalar(select(Customer.id)) + 1,
                name=request.form.get("name"),
                birthday=request.form.get("birthday"),
                address=request.form.get("address"),
                postcode= convert_postcode(request.form.get("postcode")),
            )
            db_session.add(customer)
            db_session.flush()

        return redirect(url_for('order_success'))

   # except Exception as e:
       # return render_template('error.html', message=str(e))



@app.route("/checkout/order_success", methods=["GET", "POST"])
def order_success():
    return render_template("order_success.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not fsession.get("admin"):
        return redirect("/admin/login")
    return render_template("index.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    fsession.pop("admin", None)
    fsession.pop("username", None)
    fsession.pop("password", None)
    fsession["cart"] = []
    fsession.modified = True
    return redirect(url_for("index"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    return render_template("login_admin.html")


@app.route("/admin/login/submit", methods=["GET", "POST"])
def admin_login_submit():
    fsession["username"] = request.form["username"]
    fsession["password"] = (request.form["password"])
    fsession["admin"] = True
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

