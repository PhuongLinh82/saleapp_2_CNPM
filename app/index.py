from flask import render_template, request, redirect, jsonify, session
import dao
import utils
from app import app, login
from flask_login import login_user

@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')

    cates = dao.load_categories()
    prods = dao.load_products(kw, cate_id)
    return render_template('index.html', categories=cates, products=prods)

@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@app.route("/api/cart", methods=['post'])
def add_to_cart():
    '''
    {
        "cart" : {
            "1": {
                "id": "1",
                "name": "abc",
                "price": 123,
                "quantity": 1
            }, "2": {
                "id": "2",
                "name": "abc",
                "price": 123,
                "quantity": 1
            }
        }
    }
    :return:
    '''
    data = request.json

    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart:
        cart[id]['quantity'] += 1
    else: # sp chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart
    print(cart)

    return jsonify(utils.count_cart(cart))

@app.route('/cart')
def cart():
    return render_template('cart.html')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)