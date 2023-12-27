from app.models import Category, Product, User, Receipt, ReceiptDetail
from app import db, app
import hashlib
from flask_login import current_user


def get_categories():
    return Category.query.all()


def get_products(kw, cate_id, page=None):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size

        return products.slice(start, start * page_size)

    return products.all()

def count_product():
    return Product.query.count()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password,
             avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    db.session.add(u)
    db.session.commit()

def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        #db.session.