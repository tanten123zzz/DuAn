from QLNhaSach.models import Category, Product, Tag, User, UserRole, Inventory, Receipt, ReceiptDetails, \
    InventoryDetails, Author, Regulation
from QLNhaSach import db, app, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, render_template, request
from datetime import datetime


admin = Admin(app=app, name='QUẢN TRỊ BÁN SÁCH', base_template='admin/base.html')


class Employee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.EMPLOYEE


class Admin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CategoryView(Admin):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    form_excluded_columns = ['InventoryDetails']


class UserView(Admin):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    form_excluded_columns = ['comments', 'inventorys', 'receipts']


class ProductView(Admin):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá',
        'soluongton': 'Số lượng tồn',
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class Base(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(Base):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class InventoryView(Admin):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    column_exclude_list = ['InventoryDetails']
    form_excluded_columns = ['InventoryDetails']
    column_searchable_list = ['user_id']
    column_labels = {
        'name': 'Nhập số phiếu',
        'user': 'Tên người dùng',
    }


class InventoryDetailsView(Admin):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    column_exclude_list = ['inventory']
    column_searchable_list = ['product_id']
    column_labels = {
        'product': 'Sách',
        'author': 'Tác giả',
        'category': 'Thể loại',
        'quantity': 'Số lượng',
        'inventory': 'Phiếu nhập'
    }


class StatsView(Base):
    @expose('/')
    def index(self):
        Doanhthu = dao.ThongKe_DoanhThu(kw=request.args.get('kw'), from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'),
                                  year=request.args.get('year', datetime.now().year))

        Tansuat = dao.ThongKe_TanSuat( year=request.args.get('year', datetime.now().year))
        return self.render('admin/stats.html', Doanhthu = Doanhthu , Tansuat = Tansuat)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class HoaDonView(BaseView):
    @expose('/')
    def index(self):
        eyyo = dao.stats_hoadon()
        return self.render('admin/receipt.html', eyyo=eyyo)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.EMPLOYEE


class SectionProduct(BaseView):
    @expose('/')
    def index(self):
        p = dao.get_section_product()
        qd = dao.get_quidinh()
        return self.render('admin/phieunhap.html', product=p, quidinh=qd)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class QuiDinhView(Admin):
    create_modal = False
    can_create = False


admin.add_view(CategoryView(Category, db.session, name='Danh mục'))
admin.add_view(Admin(Author, db.session, name='Tác giả'))
admin.add_view(ProductView(Product, db.session, name='Sản phẩm'))
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(InventoryView(Inventory, db.session, name='Phiếu nhập'))
admin.add_view(SectionProduct(name='Chi tiết phiếu nhập'))
admin.add_view(QuiDinhView(Regulation, db.session, name='Qui định'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(HoaDonView(name="Tính tiền"))
admin.add_view(LogoutView(name='Đăng xuất'))
