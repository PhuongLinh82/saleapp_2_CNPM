from flask import render_template, request, redirect, jsonify, session, math
import dao
import utils
from app import app, login
from flask_login import login_user, logout_user

@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    cates = dao.get_categories()
    prods = dao.get_products(kw, cate_id, page)

    num = dao.count_product()

    return render_template('index.html', products=prods,
                           pages=math.ceil(num/app.config['PAGE_SIZE']))

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

@app.route('/login', methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__(('POST')):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('login.html')

@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect('/login')

@app.route('/register', method=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password, avatar=None)
            except Exception as ex:
                print(str(ex))
                err_msg = 'Hệ thống đang bị lỗi'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp'
    return redirect('/register.html')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_response():
    return {
        'categories': dao.get_categories(),
        'cart': utils.count_cart(session.get('cart'))
    }


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)