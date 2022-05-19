import re
from flask import render_template, url_for, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, mail
from flask import render_template, Blueprint, url_for, flash, redirect, request
from app.Users.utils import save_postsImage
from app.models import Receipts,Notice
from app.Posts.forms import ReceiptForm,NoticeForm


posts = Blueprint('posts', __name__)


@posts.route('/create/receipt', methods=['POST', 'GET'])
@login_required
def create():
    form = ReceiptForm()
    if form.validate_on_submit():
        picture=save_postsImage(form.receipt_image.data)

        receipt = Receipts(
           account_number=form.account_number.data,user_id=current_user.id,
            amount=form.amount.data,receipt_image=picture,date_paid=form.date_paid.data)
        db.session.add(receipt)
        db.session.commit()
        flash('your receipt has been uploaded successfully')
        return redirect(url_for('main.home'))
    return render_template('receipts.html', form=form, title="New receipt")


@posts.route('/all/receipts',methods=['POST','GET'])
@login_required
def all_receipts():
  receipt=Receipts.query.all()
  for r in receipt:
    image_file= url_for('static',filename='posts/'+r.receipt_image)

    r.receipt_image= image_file
  return render_template('allreceipts.html',receipt=receipt)


@posts.route('/notice',methods=['GET', 'POST'])
@login_required
def notice():
    form = NoticeForm()
    if form.validate_on_submit():

        notice = Notice(title=form.title.data,content=form.content.data,user_id=current_user.id,)
        db.session.add(notice)
        db.session.commit()
        flash('your notice has been uploaded successfully')
        return redirect(url_for('main.home'))
    return render_template('notice.html', form=form, title="New Notice")

