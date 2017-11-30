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
def bounty():
    bountys = Bountyissue.select()
    return render_template('bountys.html', bountys = bountys)