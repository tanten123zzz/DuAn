from QLNhaSach.models import User
from QLNhaSach import dao,db


def cart_stats(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }


def product_stats(product):
    total_soluongton = 0
    if product:
        for p in product.values():
            total_soluongton = p['soluongton']
    return {
        'total_soluongton': total_soluongton
    }


def get_user_by_id(user_id):
    return User.query.get(user_id)



