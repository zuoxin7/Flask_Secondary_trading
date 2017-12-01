from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
import requests
import hashlib
from flask import current_app, request
from requests.exceptions import ConnectionError, HTTPError
from utils.identicon import IdenticonSVG

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
    avatar_hash = pw.CharField(32, null=True)
    password_hash = pw.CharField(128)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='404', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'

        if not self.avatar_hash:
            self.avatar_hash = hashlib.md5(
                self.email.lower().encode('utf-8')).hexdigest()
            self.save()
        hash = self.avatar_hash
        gravatar_url = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
        return gravatar_url

    def avatar(self, size=100, **kwargs):
        gravatar_url = self.gravatar(size)
        try:
            r = requests.get(gravatar_url)
            r.raise_for_status()
        except (ConnectionError, HTTPError):
            i = IdenticonSVG(self.avatar_hash, size=size, **kwargs)
            gravatar_url = 'data:image/svg+xml;text,{0}'.format(i.to_string(True))

        return gravatar_url

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


class Post(db.Model):
    body = pw.TextField(null=True)
    timestamp = pw.DateTimeField(index=True, default=datetime.utcnow)
    author = pw.ForeignKeyField(User, related_name='posts', null=True)

    class Meta:
        db_table = 'posts'