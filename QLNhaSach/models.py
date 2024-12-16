from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from QLNhaSach import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)
    InventoryDetails = relationship('InventoryDetails', backref='category', lazy=True)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('name', Integer, nullable=False),
                    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    authors = relationship('Author', backref='product', lazy=True)
    # author_id = Column(Integer, ForeignKey(Author.id), nullable=False)

    InventoryDetails = relationship('InventoryDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)
    soluongton = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    joined_date = Column(DateTime, default=datetime.now())
    inventorys = relationship('Inventory', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    active = Column(Boolean, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)

    def __int__(self):
        return self.id


class Author(BaseModel):
    name = Column(String(50), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    InventoryDetails = relationship('InventoryDetails', backref='author', lazy=True)

    def __str__(self):
        return self.name


class Inventory(BaseModel):
    name = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    InventoryDetails = relationship('InventoryDetails', backref='inventory', lazy=True)


class InventoryDetails(BaseModel):
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    inventory_id = Column(Integer, ForeignKey(Inventory.id), nullable=False)
    quantity = Column(Integer, default=0)


class Regulation(BaseModel):
    soluongtoithieu = Column(Integer, default=0)
    soluongsach= Column(Integer, default=0)
    update_time = Column(Integer, default=0)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        c1 = Category(name='Sách giáo khoa')
        c2 = Category(name='Sách lập trình')
        c3 = Category(name='Sách kinh tế')
        db.session.add_all([c1, c2, c3])
        db.session.commit()

        p1 = Product(name='Sách lập trình cơ bản SQL', price=100000, description='Lập trình',
                     image='https://m.media-amazon.com/images/I/61IvZ9eG91L._AC_UL320_.jpg', category_id=2,
                     soluongton=2)
        p2 = Product(name='Sách lập trình cơ bản Go', price=150000, description='Lập trình',
                     image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg', category_id=2,
                     soluongton=2)
        p3 = Product(name='Sách Computer Science', price=800000, description='Giáo khoa',
                     image='https://m.media-amazon.com/images/I/61fFh20AhQL._AC_UL320_.jpg', category_id=1,
                     soluongton=2)
        p4 = Product(name='Sách dạy con làm giàu', price=1400000, description='Kinh tế',
                     image='https://www.nxbtre.com.vn/Images/Book/copy_16_nxbtre_thumb_05062017_110640.jpg',
                     category_id=3, soluongton=2)
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name="Vinh", username='admin', password=password,
                 user_role=UserRole.ADMIN,
                 image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg')
        db.session.add(u)
        db.session.commit()

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name="Khe", username='employee', password=password,
                 user_role=UserRole.EMPLOYEE,
                 image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg')
        db.session.add(u)
        db.session.commit()

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name="Nhan", username='user', password=password,
                 user_role=UserRole.USER,
                 image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg')
        db.session.add(u)
        db.session.commit()

        a1 = Author(name='Vĩnh bình tĩnh', product_id=1)
        a2 = Author(name='Khê mãi mê', product_id=2)
        a3 = Author(name='Nhân nhúng nhảy', product_id=3)
        db.session.add_all([a1, a2, a3])
        db.session.commit()

        pn1 = Inventory(user_id=1)
        pn2 = Inventory(user_id=2)

        db.session.add_all([pn1, pn2])
        db.session.commit()

        qd = Regulation(soluongtoithieu=150, soluongsach=300, update_time=48)
        db.session.add(qd)
        db.session.commit()