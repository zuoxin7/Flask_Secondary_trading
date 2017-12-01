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
    owner = pw.CharField(64)
    name = pw.CharField(64, null=True)
    introduction = pw.CharField(64, null=True)
    category = pw.CharField()
    price = pw.FloatField()
    good_trade = pw.BooleanField(default=False)
    good_tradeID = pw.CharField(null=True)
    good_ifcomment = pw.BooleanField(default=False)
    good_comment = pw.CharField(null=True)
    imagefile = pw.CharField(64, null=True)

    def __repr__(self):
        return '<GoodsissueGoods %r>' % self.id

    class Meta:
        db_table = 'goods'

class Bountyissue(db.Model):
    wanter = pw.CharField(64)
    name = pw.CharField(64, null=True)
    introduction = pw.CharField(64, null=True)
    price = pw.FloatField()
    bounty_trade = pw.BooleanField(default=False)
    bounty_tradeID = pw.CharField(null=True)
    bounty_ifcomment = pw.BooleanField(default=False)
    bounty_comment = pw.CharField(null=True)

    def __repr__(self):
        return '<Bountyissue %r>' % self.id

    class Meta:
        db_table = 'bountys'