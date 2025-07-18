import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.utils.notifications import get_notification_preferences, set_notification_preference
from app.models.notification import NotificationType
from app.models import User, Job, Event, Testimonial, News, Message, RSVP
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.utils.forms import EditProfileForm
from app.models import User

bp = Blueprint('profile', __name__)

__all__ = ['bp']


@bp.route('/profile')
@bp.route('/')
@login_required
def index():
    user = current_user
    jobs = user.jobs_posted.order_by(Job.created_at.desc()).limit(3)
    events = user.events_created.order_by(Event.created_at.desc()).limit(3)
    testimonials = user.testimonials.order_by(Testimonial.created_at.desc()).limit(3)
    news_posts = user.news_posts.order_by(News.created_at.desc()).limit(3)
    sent_messages = sorted(user.sent_messages, key=lambda m: m.sent_at, reverse=True)[:2]
    received_messages = sorted(user.received_messages, key=lambda m: m.sent_at, reverse=True)[:2]
    rsvps = user.rsvps.order_by(RSVP.rsvp_date.desc()).limit(3)
    return render_template(
        'profile/index.html',
        user=user,
        jobs=jobs,
        events=events,
        testimonials=testimonials,
        news_posts=news_posts,
        sent_messages=sent_messages,
        received_messages=received_messages,
        rsvps=rsvps
    )

@bp.route('/profile/<int:user_id>')
def view(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return render_template('profile/view.html', user=user)

@bp.route('/preferences/notifications', methods=['GET', 'POST'])
@login_required
def notification_preferences():
    if request.method == 'POST':
        for notif_type in NotificationType:
            enabled = request.form.get(f'enabled_{notif_type.value}') == '1'
            set_notification_preference(current_user.id, notif_type, enabled)
        flash('Notification preferences updated.', 'success')
        return redirect(url_for('profile.notification_preferences'))
    preferences = get_notification_preferences(current_user.id)
    return render_template('profile/preferences.html', preferences=preferences)

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
