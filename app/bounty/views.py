from flask import render_template, redirect, request, url_for, flash, session
from flask import make_response
from flask_login import current_user
from . import bounty
from ..models import User, Bountyissue
from .forms import BountyForm, BountyComment
from werkzeug.utils import secure_filename


@bounty.route('/issue_bounty', methods=['GET', 'POST'])
def issue_bounty():
    form = BountyForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('app/static/upload/' + filename)
        usernum = User.update(num_pushbounty=User.num_pushbounty + 1, num=User.num + 1).where(
            User.username == current_user.username).execute()
        bounty = Bountyissue(wanter=current_user.username,
                             name=form.name.data,
                             introduction=form.introduction.data,
                             price=form.price.data,
                             imagefile=secure_filename(form.image.data.filename))
        try:
            bounty.save()
            flash('你已经发布成功')
            return redirect('./bounty')
        except:
            flash("发布失败")
    return render_template('add_bounty.html', form=form)


@bounty.route('/bounty', methods=['GET', 'POST'])
def bounty_list():
    bountys = Bountyissue.select().where(Bountyissue.bounty_trade == False)
    useremail = []
    for i in bountys:
        use = User.select().where(i.wanter == User.username)
        for t in use:
            useremail.append(t.email)
    return render_template('bountys.html', bountys=bountys, useremail=useremail)


@bounty.route('/bountyhistory', methods=['GET', 'POST'])
def bountyhistory():
    mybounds = Bountyissue.select().where(Bountyissue.wanter == current_user.username)
    mygetbountys = Bountyissue.select().where(Bountyissue.bounty_tradeID == current_user.username)
    return render_template('bounty_history.html', mybounds=mybounds, mygetbountys=mygetbountys)


# 领取操作
@bounty.route('/bountyscore/<bountyid>', methods=['GET', 'POST'])
def getbounty(bountyid):
    getbountys = Bountyissue.update(bounty_trade=True, bounty_status=2, bounty_tradeID=current_user.username).where(
        Bountyissue.id == bountyid).execute()
    usernum = User.update(num_getbounty=User.num_getbounty + 1, num=User.num + 1).where(
        User.username == current_user.username).execute()
    flash('你已经完成领取')
    return redirect('./bounty')


# 悬赏回馈
@bounty.route('/bountycomment/<bountyid>', methods=['GET', 'POST'])
def bountycomment(bountyid):
    form = BountyComment()
    bountys = Bountyissue.select().where(Bountyissue.id == bountyid)
    if form.validate_on_submit():
        Bounty_comment = Bountyissue.update(bounty_ifcomment=True, bounty_status=3,
                                            bounty_comment=form.bounty_comment.data).where(
            Bountyissue.id == bountyid).execute()
        flash('你已经完成悬赏反馈')
        return redirect('./bountyhistory')
    return render_template('Bounty_comment.html', bountys=bountys, form=form)
