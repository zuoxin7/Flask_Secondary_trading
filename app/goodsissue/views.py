from flask import render_template, redirect, request, url_for, flash, session
from flask import make_response
from flask_login import  current_user
from werkzeug.utils import secure_filename
from . import goodsissue
from ..models import User, GoodsissueGoods
from .forms import GoodsForm


@goodsissue.route('/issue_good', methods=['GET', 'POST'])
def issue_good():
    form = GoodsForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('app/static/upload/' + filename)
        good = GoodsissueGoods(owner=current_user.username,
                               name=form.name.data,
                               introduction=form.introduction.data,
                               category=form.category.data,
                               price=form.price.data,
                               imagefile=secure_filename(form.image.data.filename))
        try:
            good.save()
            flash('你已经发布成功')
            return redirect(url_for('main.index'))
        except:
            flash("发布失败")
    return render_template('add_good.html', form=form)



@goodsissue.route('/goods', methods=['GET', 'POST'])
def goods():
    goods = GoodsissueGoods.select()
    return render_template('goods.html', goods = goods)