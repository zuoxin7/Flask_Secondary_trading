from flask import render_template, session, redirect, url_for
from .forms import PostForm
from flask_login import login_required, current_user
from . import main
from ..models import User, Post
from .. import db

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if (current_user.is_authenticated and form.validate_on_submit()):
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        post.save()
        return redirect(url_for('.index'))
    posts = Post.select().order_by(Post.timestamp.desc())
    return render_template('index.html', form=form, posts=posts)

