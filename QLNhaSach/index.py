from flask import render_template, request, redirect, session, jsonify
from QLNhaSach import app, dao, admin, login, utils, controllers
from flask_login import login_user, logout_user, login_required

from QLNhaSach.dao import get_product_by_id
from QLNhaSach.decorators import annonymous_user
import cloudinary.uploader


app.add_url_rule('/chitietphieunhap', 'product', controllers.chitietphieunhap)
app.add_url_rule('/api/chitietphieunhap', 'add-product', controllers.add_to_product, methods=['post'])
app.add_url_rule('/chitietphieunhap/<product_id>', 'update-product', controllers.update_product, methods=['put'])
app.add_url_rule('/chitietphieunhap/<product_id>', 'delete-product', controllers.delete_product, methods=['delete'])
app.add_url_rule('/receiptdetail/<int:receipt_id>', 'receipt-detail', controllers.chitiethoadon)
app.add_url_rule('/<int:receipt_id>', 'update-receipt-detail', controllers.update_receipt_detail, methods=['update'])
app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/products/<int:product_id>', 'product-detail', controllers.details)
app.add_url_rule('/login-admin', 'login-admin', controllers.login_admin, methods=['post'])
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/cart', 'cart', controllers.cart)
app.add_url_rule('/api/cart', 'add-cart', controllers.add_to_cart, methods=['post'])
app.add_url_rule('/api/cart/<product_id>', 'update-cart', controllers.update_cart, methods=['put'])
app.add_url_rule('/api/cart/<product_id>', 'delete-cart', controllers.delete_cart, methods=['delete'])
app.add_url_rule('/api/pay_online', 'pay_online', controllers.pay_online)
app.add_url_rule('/api/pay_offline', 'pay_offline', controllers.pay_offline)
app.add_url_rule('/api/save_phieunhap', 'luu-chitiet', controllers.LuuPhieuNhap)


@app.context_processor
def common_attr():
    categories = dao.load_categories()

    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
@app.route('/product/<int:id>')
def product_detail(id):
    # Giả sử bạn lấy dữ liệu sản phẩm từ cơ sở dữ liệu
    product = get_product_by_id(id)
    if not product:
        return "Sản phẩm không tồn tại", 404
    return render_template('product_detail.html', product=product)
if __name__ == "__main__":
    app.run(debug=True)