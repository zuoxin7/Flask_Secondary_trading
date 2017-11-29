from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

import peewee as pw

from . import db
from . import login_manager


class Role(db.Model):
    name = pw.CharField(64, unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

    class Meta:
        db_table = 'roles'


class User(UserMixin, db.Model):
    email = pw.CharField(64, unique=True, index=True)
    phone = pw.CharField(11, index=True)
    pay = pw.CharField(64, index=True)
    username = pw.CharField(64, unique=True, index=True)
    academy = pw.CharField(64, index=True, null=True)
    grade = pw.CharField(64, index=True, null=True)
    major = pw.CharField(64, index=True, null=True)
    role = pw.ForeignKeyField(Role, related_name='users', null=True)
    password_hash = pw.CharField(128)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    class Meta:
        db_table = 'users'


@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id == int(user_id)).first()

#商品表
class GoodsissueGoods(db.Model):
    id = pw.IntegerField(primary_key=True)  # AutoField?
    owner = pw.ForeignKeyField(User, null=True)
    name = pw.CharField(64, null=True)
    introduction = pw.CharField(64, null=True)
    price = pw.FloatField(null=True)
    imagefile = pw.CharField(64, null=True)

    class Meta:
        managed = False
        db_table = 'goodsissue_goods'

#商品发布表
class GoodsissueIssuer(db.Model):
    id = pw.IntegerField(primary_key=True)  # AutoField?
    uid = pw.ForeignKeyField(User, db_column='uid', null=True)
    goods = pw.ForeignKeyField(GoodsissueGoods, null=True)
    issuedate = pw.DateTimeField(db_column='issueDate', null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'goodsissue_issuer'

#商品销售表
class GoodsissueSaler(db.Model):
    id = pw.IntegerField(primary_key=True)  # AutoField?
    buyer = pw.ForeignKeyField(User, null=True)
    goods_id = pw.IntegerField(null=True)
    tradedate = pw.DateTimeField(db_column='tradeDate', null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'goodsissue_saler'
