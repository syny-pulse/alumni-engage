from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.utils.forms import EditProfileForm
from app.models import User

bp = Blueprint('profile', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('profile.edit_profile'))

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get_or_404(current_user.id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.current_job_title = form.current_job.data
        user.address = form.address.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile.edit_profile'))
    return render_template('profile/edit.html', title='Edit Profile', form=form)




