from flask import render_template, redirect, request, url_for, flash, session
from flask import make_response
from flask_login import  current_user
from . import bounty
from ..models import User, Bountyissue
from .forms import BountyForm


@bounty.route('/issue_bounty', methods=['GET', 'POST'])
def issue_bounty():
    form = BountyForm()
    if form.validate_on_submit():
        bounty = Bountyissue(wanter=current_user.username,
                               name=form.name.data,
                               introduction=form.introduction.data,
                               price=form.price.data)
        try:
            bounty.save()
            flash('你已经发布成功')
            return redirect(url_for('main.index'))
        except:
            flash("发布失败")
    return render_template('add_bounty.html', form=form)


@bounty.route('/bounty', methods=['GET', 'POST'])
def bounty_list():
    bountys = Bountyissue.select().where(Bountyissue.bounty_trade == False)
    return render_template('bountys.html', bountys = bountys)


@bounty.route('/bountyhistory', methods=['GET', 'POST'])
def bountyhistory():
    mybounds = Bountyissue.select().where(Bountyissue.wanter == current_user.username)
    mygetbountys = Bountyissue.select().where(Bountyissue.bounty_tradeID == current_user.username)
    return render_template('bounty_history.html', mybounds=mybounds, mygetbountys=mygetbountys)


#领取操作
@bounty.route('/bountyscore/<bountyid>', methods=['GET', 'POST'])
def getbounty(bountyid):
    getbountys = Bountyissue.update(bounty_trade = True, bounty_tradeID = current_user.username).where(Bountyissue.id == bountyid).execute()
    flash('你已经完成领取')
    return render_template('index.html')