import datetime

from flask import Flask, request, jsonify, render_template, session as fsession, redirect, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import func

from models import Base, Pizza, Customer, Order, OrderedPizza  # import your SQLAlchemy 2.0 models
from config import Config
from contextlib import contextmanager
import utils


app = Flask(__name__)
app.config.from_object(Config)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)

# Thread-safe session factory
session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
db_session = scoped_session(session_factory)
session = Session(engine)



# ----------------------------------------
# Helper functions
# ----------------------------------------



def get_image(type, id):
    return "/static/images/default.jpg"


def get_description(type, id):
    return ""


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

    return render_template("menu.html", pizzas=utils.get_pizzas())

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
    try:
        item_dic = fsession["cart"]
    except:
        item_dic = []
    return render_template("checkout.html", cart_items=item_dic, total = get_total_price(item_dic))

@app.route("/checkout/remove_from_cart", methods=["GET", "POST"])
def remove_from_cart():
    deleted_item = request.form.get("item_id")
    fsession["cart"].pop(int(deleted_item)-1)
    fsession.modified = True
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



    top_pizza = []
    with db_session() as session:
        stmt = select(Pizza)

        date_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)

        top_pizzas = db_session.query(
            Pizza.name,
            func.count(OrderedPizza.pizza_id).label('total_sold')
        ).join(
            OrderedPizza, Pizza.id == OrderedPizza.pizza_id
        ).join(
            Order, OrderedPizza.order_id == Order.id
        ).filter(
            Order.timestamp >= date_month_ago
        ).group_by(
            Pizza.id, Pizza.name
        ).order_by(
            desc('total_sold')
        ).limit(3).all()


        for pizza in top_pizzas:
            countp = func.count(Pizza.id).label("count")
            top_pizza.append({
                "name": pizza.name,
                "count": countp,
                "price": pizza.price * countp,

            })

    earnings_data = []
    #data needed:
    # employee = {
    #     "id":,
    #     "name":,
    #     "age":,
    #     "gender":,
    #     "postal_code":,
    #     "earnings":[total sum]
    # }
    # The hard part:
    # everything according to filters below
    #

    try:
        filters = {
            "age_min": request.form.get("age_min"),
            "age_max": request.form.get("age_max"),
            "gender": request.form.get("gender"),
            "postal_code": request.form.get("postal_code"),
            "postal_code_range": request.form.get("postal_code_range"),
            "from_date": request.form.get("from_date"),
            "to_date": request.form.get("to_date")

        }
    except:
        filters = {
            "age_min": 0,
            "age_max": 100,
            "gender": "",
            "postal_code": 0,
            "postal_code_range": 9999,
            "from_date": None,
            "to_date": None

        }

    current_orders = []
    # data needed:
    # order = {
    #     "id":,
    #     "customer_name":,
    #     "address":,
    #     "delivery":[person],
    #     "status":,
    #     "total":[price for everything],
    #     "timestamp":
    # }
    #
    #




    return render_template("admin.html", filters=filters, )


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

