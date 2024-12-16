from QLNhaSach.models import Category, Product, User, Receipt, ReceiptDetails, Comment, Author ,Regulation, InventoryDetails,Inventory
from flask_login import current_user
from sqlalchemy import func
from QLNhaSach import db
from sqlalchemy.sql import extract
from datetime import datetime
import hashlib

from twilio.rest import Client

account_sid = 'ACd0b4da8ac3a746f969053e85e9462d66'

auth_token = '49c4d1131e8fc84ede723dba8bb3fbcb'

twilio_number = '+18087551692'

my_phone_number = '+84987135520'

client = Client(account_sid, auth_token)


def get_section_product():
    query = db.session.query(Product.name, Category.name, Product.soluongton, Author.name, Product.id, Author.id,
                             Category.id) \
        .join(Product, Product.category_id.__eq__(Category.id)) \
        .join(Author, Author.product_id.__eq__(Product.id))
    return query.all()


def load_categories():
    return Category.query.all()


def get_by_id_user(user_id):
    return User.query.get(user_id)


def load_receipt_by_user(user_id):
    query = db.session.query(Receipt.created_date, ReceiptDetails.quantity, Product.name, ReceiptDetails.active) \
        .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
        .filter(Receipt.user_id.__eq__(user_id)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id))

    return query.all()


def load_products(cate_id=None, kw=None):
    query = Product.query

    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.filter(Product.soluongton != 0).all()


def chitietphieunhap(product_id):
    query = Product.query

    if product_id:
        query = db.session.query(Product.id, Product.name, Product.soluongton) \
            .filter(Product.id.__eq__(product_id))

    return query.all()


def get_value_product(product_id):
    query = Product.query

    if product_id:
        query = db.session.query(Product.soluongton) \
            .filter(Product.id.__eq__(product_id))
    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_receipt_by_id(receipt_id):
    return Receipt.query.get(receipt_id)


def get_receipt_detail_by_id(receipt_id):
    query = db.session.query(ReceiptDetails.receipt_id, ReceiptDetails.active, Product.name, ReceiptDetails.quantity, Product.soluongton, Product.id) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
        .filter(ReceiptDetails.receipt_id.__eq__(receipt_id))

    return query.all()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, image=avatar)
    db.session.add(u)
    db.session.commit()


def save_receipt_online(cart):
    if cart:
        r = Receipt(created_date=datetime.now(), user=current_user)
        db.session.add(r)
        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'], active=1)
            post_query = db.session.query(Product).filter(Product.id.__eq__(c['id']))
            post_query.update({'soluongton': c['soluongton']}, synchronize_session=False)
            db.session.add(d)

        # client.messages.create(
        #     body=current_user.name + " đã thanh toán thành công!!",
        #     from_=twilio_number,
        #     to=my_phone_number)

        db.session.commit()


def save_receipt_offline(cart):
    if cart:
        r = Receipt(created_date=datetime.now(), user=current_user)
        db.session.add(r)
        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'], active=0)
            post_query = db.session.query(Product).filter(Product.id.__eq__(c['id']))
            post_query.update({'soluongton': c['soluongton']}, synchronize_session=False)
            db.session.add(d)

        db.session.commit()


def save_phieunhap(product):
    if product:
        user = Inventory(user=current_user)
        db.session.add(user)
        for p in product.values():
            d = InventoryDetails(product_id=p['id'],
                                 category_id=p['theloai'],
                                 author_id=p['tacgia'],
                                 inventory=user,
                                 quantity=p['soluongton'])

            post_query = db.session.query(Product).filter(Product.id.__eq__(p['id']))
            post_query.update({'soluongton': p['soluongton']}, synchronize_session=False)

            db.session.add(d)
        db.session.commit()


def get_product(receipt_id):
    query = db.session.query(ReceiptDetails.id, Product.name, ReceiptDetails.quantity, ReceiptDetails.active) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
        .filter(ReceiptDetails.id.__eq__(receipt_id))
    return query.all()


def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id)) \
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True) \
        .group_by(Category.id).all()





def stats_hoadon():
    query = db.session.query(Receipt.id, Receipt.created_date, User.name,
                             func.sum(ReceiptDetails.price * ReceiptDetails.quantity), ReceiptDetails.active) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
        .join(User, User.id.__eq__(Receipt.user_id))
    return query.group_by(Receipt.id).all()


def get_quidinh():
    return Regulation.query.all()


def ThongKe_DoanhThu(kw=None, from_date=None, to_date=None, year=None):
    query = db.session.query(Category.id, Category.name,
                             func.sum(ReceiptDetails.price * ReceiptDetails.quantity), extract('month', Receipt.created_date)) \
        .join(Product, Product.category_id.__eq__(Category.id)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
        .join(Receipt, Receipt.id.__eq__(ReceiptDetails.receipt_id)) \
        .filter(extract('year', Receipt.created_date) == year) \
        .group_by(extract('month', Receipt.created_date))

    if kw:
        query = query.filter(Category.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Category.id).order_by(extract('month', Receipt.created_date)).all()


def ThongKe_TanSuat(year):
    query = db.session.query(Product.id, Product.name, Category.name, ReceiptDetails.quantity,
                             ReceiptDetails.quantity / func.sum(ReceiptDetails.quantity),
                             extract('month', Receipt.created_date)) \
        .join(Product, Product.category_id.__eq__(Category.id)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
        .filter(extract('year', Receipt.created_date) == year) \
        .group_by(extract('month', Receipt.created_date))

    return query.group_by(Product.name).order_by(extract('month', Receipt.created_date)).all()


if __name__ == '__main__':
    from QLNhaSach import app

    with app.app_context():
        print(count_product_by_cate())



