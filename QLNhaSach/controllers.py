import flask
from flask import render_template, request, redirect, session, jsonify
from QLNhaSach import app, dao, admin, login, utils
from flask_login import login_user, logout_user, login_required
from QLNhaSach.decorators import annonymous_user
import cloudinary.uploader
import re
# import mysql.connector
#
# mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='03112002', database='cs01saled')
# mycursor = mydb.cursor()
# mycursor.execute('set global event_scheduler=on')
# code = "create event if not exists delete_event ON schedule every 10 second starts current_timestamp() do delete from "
# code_tmp = "receipt_details where active = 0 and receipt_id in (select id from receipt where created_date < Date_sub(now(),interval 48 hour));"
# mycursor.execute(code + code_tmp)
# code2 = "create event if not exists delete_event2 ON schedule every 20 second starts current_timestamp() do "
# code2_tmp = "delete from receipt where id not in (select receipt_id from receipt_details);"
# mycursor.execute(code2 + code2_tmp)


def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id, kw)
    return render_template('index.html', products=products)


def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


def chitiethoadon(receipt_id):
    receipt = dao.get_receipt_by_id(receipt_id)
    receipt_tmp = re.search(r'\d+', str(receipt))
    rec = dao.get_receipt_detail_by_id(receipt_tmp.group())
    return render_template('receiptdetail.html', receiptdetails=rec)


def update_receipt_detail(receipt_id):
    # re = 'UPDATE receipt_details SET active = 1 WHERE receipt_details.receipt_id = ' + str(receipt_id)
    # mycursor.execute(re)
    # mydb.commit()
    print(receipt_id)


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get("next")
            return redirect(n if n else '/')

    return render_template('login.html')


def logout_my_user():
    logout_user()
    return redirect('/login')


def cart():
    return render_template('cart.html')


def chitietphieunhap():
    qd = dao.get_quidinh()
    return render_template('chitietphieunhap.html', quidinh=qd)


def add_to_cart():
    data = request.json
    id = str(data['id'])
    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}
    if id in cart:
        if cart[id]['soluongton'] > 0:
            cart[id]['quantity'] += 1
            cart[id]['soluongton'] -= 1
        else:
            cart[id]['quantity'] = cart[id]['quantity']
            cart[id]['soluongton'] = cart[id]['soluongton']
    else:
        name = data['name']
        price = data['price']
        soluongton = data['soluongton']
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1,
            "soluongton": soluongton - 1
        }
    session[key] = cart
    return jsonify(utils.cart_stats(cart))


def add_to_product():
    key = app.config['PRODUCT_KEY']
    product = session[key] if key in session else {}
    data = request.json
    id = str(data['id'])
    name = data['name']
    soluongton = data['soluongton']
    theloai = data['theloai']
    tacgia = data['tacgia']
    product[id] = {
        "id": id,
        "name": name,
        "soluongton": soluongton,
        "theloai": theloai,
        "tacgia": tacgia
    }
    session[key] = product
    return jsonify(utils.product_stats(product))


def update_product(product_id):
    key = app.config['PRODUCT_KEY']
    product = session.get(key)
    if product_id in product:
        product[product_id]['soluongton'] = int(request.json['soluongton'])
    session[key] = product
    return jsonify(utils.product_stats(product))


def delete_product(product_id):
    key = app.config['PRODUCT_KEY']
    product = session.get(key)

    if product and product_id in product:
        del product[product_id]

    session[key] = product

    return jsonify(utils.product_stats(product))


def update_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def delete_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@login_required
def pay_online():
    key = app.config['CART_KEY']
    cart = session.get(key)
    if cart:
        try:
            dao.save_receipt_online(cart=cart)

        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})


@login_required
def pay_offline():
    key = app.config['CART_KEY']
    cart = session.get(key)
    if cart:
        try:
            dao.save_receipt_offline(cart=cart)

        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})


def LuuPhieuNhap():
    key = app.config['PRODUCT_KEY']
    product = session.get(key)
    print(product)
    if product:
        try:
            dao.save_phieunhap(product=product)

        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})
