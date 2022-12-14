from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import db
from sqlalchemy import desc
from app.models import Statia
from app.models import User, Likes, Comments
from app.user.home.forms import StatiaForm

auth_home_blueprint = Blueprint('auth_home', __name__, template_folder='templates')


@auth_home_blueprint.route('/welcome-home', methods=['GET', 'POST'])
@login_required
def create():
    users = User.query.all()
    form = StatiaForm()
    data = []
    post = Statia.query.all()
    comments = Comments.query.all()
    liked_by = []

    for i in post:
        for j in i.likes:
            print(j.user.username)

    if form.validate_on_submit():
        content = form.content.data
        user_id = current_user.id
        cont = Statia(content=content, user_id=user_id)
        db.session.add(cont)
        db.session.commit()

    for i in Statia.query.order_by(desc(Statia.id)).all():
        data.append({

            'id': i.id,
            'username': i.user.username,
            'content': i.content,
            'user_id': i.user_id,
            'user_img': i.user.profile_pic,
            'comments': i.comments,
            'likes': i.likes,
            'edited':i.edited,
            'created_post_date': i.created_post_date,

        })


    return render_template('auth_home.html', form=form, data=data, users=users, comments=comments)


@auth_home_blueprint.route('/delete-post/<post_id>', methods=['GET'])
def delete_post(post_id):
    post = Statia.query.filter_by(id=post_id)

    if not post:
        flash('post does not exists')
    else:
        for info in post:
            db.session.delete(info)
            db.session.commit()

    return redirect(url_for('auth_home.create'))


@auth_home_blueprint.route('/edit-post/<post_id>', methods=['POST'])
def edit_post(post_id):
    post = Statia.query.filter_by(id=post_id).first()

    update_text = request.form['updated']

    if not post:
        flash('post does not exists')
    else:
        post.content = update_text
        post.edited = True
        db.session.commit()
    return redirect(url_for('auth_home.create'))


@auth_home_blueprint.route('/like-post/<post_id>', methods=['GET'])
@login_required
def like(post_id):
    user = User.query.all()
    post = Statia.query.filter_by(id=post_id)
    like = Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if not post:
        flash('Post does not exist')

    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        likes = Likes(user_id=current_user.id, post_id=post_id)
        db.session.add(likes)
        db.session.commit()

    return redirect(url_for('auth_home.create'))


@auth_home_blueprint.route('/add-comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    text = request.form.get('text')

    if not text:

        flash('comment cannot be empty')
    else:
        post = Statia.query.filter_by(id=post_id)

        if post:
            print(text)
            comment = Comments(text=text, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()

        else:
            flash('post does not exist')

    return redirect(url_for('auth_home.create'))


@auth_home_blueprint.route('/delete-comment/<comment_id>', methods=['GET'])
@login_required
def delete_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('auth_home.create'))


@auth_home_blueprint.route('/edit-comment/<comment_id>', methods=['POST'])
@login_required
def edit_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()

    updated_text = request.form.get('updated-text')


    if not updated_text:
        flash('comment does not exists')
    else:
        comment.text = updated_text
        comment.edited = True
        db.session.commit()

    return redirect(url_for('auth_home.create'))

