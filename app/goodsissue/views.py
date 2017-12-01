from flask import render_template, redirect, request, url_for, flash, session
from flask import make_response
from flask_login import  current_user
from werkzeug.utils import secure_filename
from . import goodsissue
from ..models import User, GoodsissueGoods
from .forms import GoodsForm,GoodComment


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


#商品列表
@goodsissue.route('/goods', methods=['GET', 'POST'])
def goods():
    goods = GoodsissueGoods.select().where(GoodsissueGoods.good_trade == False)
    return render_template('goods.html', goods=goods)

#购买记录
@goodsissue.route('/goodhistory', methods=['GET', 'POST'])
def goodhistory():
    mygoods = GoodsissueGoods.select().where(GoodsissueGoods.owner == current_user.username)
    mybuygoods = GoodsissueGoods.select().where(GoodsissueGoods.good_tradeID == current_user.username)
    return render_template('good_history.html', mygoods=mygoods, mybuygoods=mybuygoods)

#购买操作
@goodsissue.route('/goodscore/<goodid>', methods=['GET', 'POST'])
def buygood(goodid):
    # tmpgood = GoodsissueGoods.select().where(GoodsissueGoods.id == goodid)
    # if current_user.username == tmpgood.select(GoodsissueGoods.owner):
    #     print(tmpgood.select(GoodsissueGoods.owner))
    #     flash('你不能购买自己的商品')
    #     return redirect(url_for('goodsissue.goods'))
    # else:
    buygoods = GoodsissueGoods.update(good_trade = True, good_tradeID = current_user.username).where(GoodsissueGoods.id == goodid).execute()
    flash('你已经完成购买')
    return render_template('index.html')

#商品回馈
@goodsissue.route('/goodcomment/<goodid>', methods=['GET', 'POST'])
def goodcomment(goodid):
    form = GoodComment()
    goods = GoodsissueGoods.select().where(GoodsissueGoods.id == goodid)
    if form.validate_on_submit():
        Good_comment = GoodsissueGoods.update(good_ifcomment=True, good_comment=form.good_comment.data).where(GoodsissueGoods.id == goodid).execute()
        flash('你已经完成商品反馈')
        return redirect(url_for('main.index'))
    return render_template('Good_comment.html', goods=goods, form=form)