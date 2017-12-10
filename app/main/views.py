from flask import render_template, session, redirect, url_for
from .forms import PostForm
from flask_login import login_required, current_user
from . import main
from ..models import User, Post
from .. import db
from ..goodsissue.views import GoodsissueGoods
from ..bounty.views import Bountyissue


@main.route('/', methods=['GET', 'POST'])
def index():
    rank = User.select().order_by(User.num.desc())
    goods = GoodsissueGoods.select().where(GoodsissueGoods.good_trade == False).limit(3)
    bountys = Bountyissue.select().where(Bountyissue.bounty_trade == False).limit(3)
    return render_template('index.html', rank=rank, goods=goods,bountys=bountys)


@main.route('/message', methods=['GET', 'POST'])
def message():
    form = PostForm()
    if (current_user.is_authenticated and form.validate_on_submit()):
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        post.save()
        return redirect(url_for('.message'))
    posts = Post.select().order_by(Post.timestamp.desc())
    return render_template('messagepush.html', form=form, posts=posts)
