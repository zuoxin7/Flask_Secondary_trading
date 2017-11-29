from flask import render_template, redirect, request, url_for, flash, session
from flask import make_response
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from . import goodsissue
from ..models import User, GoodsissueGoods
from .forms import GoodsForm


@goodsissue.route('/issue', methods=['GET', 'POST'])
def issue():
    form = GoodsForm()
    if form.validate_on_submit():
        lenid = GoodsissueGoods.select()
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('app/static/upload/' + filename)
        good = GoodsissueGoods(id=len(lenid)+1,
                               owner=request.cookies.get('username',default='zhangjin'),
                               name=form.name.data,
                               introduction=form.introduction.data,
                               category=form.category.data,
                               price=form.price.data,
                               imagefile=filename)
        good.save()
        flash('你已经发布成功')
        return redirect(url_for('main.index'))
    return render_template('add_good.html', form=form)
