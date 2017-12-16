from flask import render_template, session, redirect, url_for
from .forms import PostForm
from flask_login import login_required, current_user
from . import main
from ..models import User, Post
from .. import db
from ..goodsissue.views import GoodsissueGoods
from ..bounty.views import Bountyissue
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


@main.route('/', methods=['GET', 'POST'])
def index():
    rank = User.select().order_by(User.num.desc())
    goods = GoodsissueGoods.select().where(GoodsissueGoods.good_trade == False).limit(3)
    bountys = Bountyissue.select().where(Bountyissue.bounty_trade == False).limit(3)
    useremail1 = []
    for i in bountys:
        use = User.select().where(i.wanter == User.username)
        for t in use:
            useremail1.append(t.email)
    useremail2 = []
    for i in goods:
        use = User.select().where(i.owner == User.username)
        for t in use:
            useremail2.append(t.email)
    return render_template('index.html', rank=rank, goods=goods, bountys=bountys, useremail1=useremail1,
                           useremail2=useremail2)


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


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/emailpost/<email>')
def postemail(email):
    ret = mail(email)
    if ret:
        return 'true'
    else:
        return 'false'


def mail(my_user):
    ret = True
    from ..email_config import email_config
    try:
        msg = MIMEText(email_config['contents'], 'plain', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", email_config['username']])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = email_config['title']  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(email_config['servers'], email_config['post'])  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(email_config['username'], email_config['password'])  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(email_config['username'], [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
