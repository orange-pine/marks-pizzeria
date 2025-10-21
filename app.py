import datetime

from flask import Flask, request, jsonify, render_template, session as fsession, redirect, url_for
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import count, func

from insert import desserts, drinks
from models import Base, DiscountCode, Pizza, Customer, Order, OrderedPizza  # import your SQLAlchemy 2.0 models
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


def get_total_price(item_dic, discount_code = None):
    total_price = 0

    for item in item_dic:
        total_price += item["price"]

    if(discount_code != None):
            if discount_code.type == "fixed":
                total_price -= discount_code.amount
            else:
                total_price *= 1 + discount_code.amount



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
    return redirect(url_for("menu"))


@app.route("/menu", methods=["GET", "POST"])
def menu():

    return render_template("menu.html", pizzas=utils.get_pizzas(), drinks = utils.get_drinks(), desserts=utils.get_desserts())

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
    return render_template("checkout.html", cart_items=item_dic, total = get_total_price(item_dic, DiscountCode(code="A", type="fixed", amount = 10)))

@app.route("/checkout/remove_from_cart", methods=["GET", "POST"])
def remove_from_cart():
    deleted_item = request.form.get("item_id")
    fsession["cart"].pop(int(deleted_item)-1)
    fsession.modified = True
    return redirect(url_for("checkout"))

@app.route("/checkout/place_order", methods=["GET", "POST"])
def place_order():

    #try:
        with db_session() as session:
            customer = utils.get_customer_by_name(request.form.get("name"))
            if customer == None:
                customer = Customer(
                name=request.form.get("name"),
                birthday=request.form.get("birthday"),
                address=request.form.get("address"),
                postcode=request.form.get("postcode"),
                )
                session.add(customer)
                session.commit()

            #Assign delivery person

            delivery_person_id = utils.get_delivery_person(customer.postcode)
            print(delivery_person_id)
            order = Order(customer_id=customer.id, timestamp=datetime.datetime.now(), status="no delivery")

            session.add(order)

            session.commit()

            (pizzas, drinks, desserts) = utils.cart_to_items(fsession["cart"], order.id)

            session.add_all(pizzas + drinks + desserts)

            session.commit()
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





    return render_template("admin.html" )


@app.route("/admin/current_orders", methods=["GET", "POST"])
def current_orders():

    with db_session() as session:

        c_orders = []

        for order in session.scalars(select(Order).where(Order.status != 'Delivered').order_by(Order.status)):
            c_orders.append({
                "id": order.id,
                "customer_name": order.customer.name,
                "address": order.customer.address,
                "delivery": order.delivery_person_id,
                "status": order.status,
                "total": order.total,
                "timestamp": order.timestamp
            })

    return render_template("current_orders.html", orders=c_orders)

@app.route("/admin/top_pizzas", methods=["GET", "POST"])
def top_pizzas():

    # query result here
    # order by count of orders
    # calculate for past 30 days
    top_pizzas_q = None

    top_pizzas = []
    the_query = "SELECT Pizza.name, COUNT(OrderedPizza.order_id) AS order_count FROM OrderedPizza JOIN Pizza ON OrderedPizza.pizza_id = Pizza.id GROUP BY OrderedPizza.pizza_id, Pizza.name;"

    with db_session() as session:
     for pizza in session.execute(select(Pizza.name.label('name'),func.count(OrderedPizza.order_id).label('count')).join(OrderedPizza).group_by(Pizza.id, Pizza.name).order_by(func.count(OrderedPizza.order_id).desc())): #for pizza in session.query(OrderedPizza).from_statement(text(the_query)).all():
        top_pizzas.append({
            "name":pizza.name,
            "count": pizza.count


        })


    return render_template("top_pizzas.html", top_pizza=top_pizzas)

@app.route("/admin/earnings", methods=["GET", "POST"])
def earnings():
    group_by = request.args.get('group_by', 'month')

    # query result here
    # name groupings "month", "age", "gender", "postcode"
    earnings_q = None

    earnings = []
    for e in earnings_q:
        current_orders.append({
            "grouping": e.group_by,
            "orders": e.count,
            "total_earnings": e.total,
            "avg_price": e.total/e.count
        })



    return render_template("earnings.html", earnings=earnings, group_by=group_by)



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
        print("Database tables created successfully!")


if __name__ == "__main__":
    app.run(debug=True, port=6009)

