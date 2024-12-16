from QLNhaSach.models import Category, Product, Tag, User, UserRole
from QLNhaSach import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect

admin = Admin(app=app, name='BÁN HÀNG', template_mode='bootstrap4')


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.EMPLOYEE


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(LogoutView(name='Đăng xuất'))