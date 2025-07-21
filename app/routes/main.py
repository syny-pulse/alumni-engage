from datetime import datetime, timezone
from flask import render_template, Blueprint
from flask_login import current_user
from app.models import News, Event, Job, User

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # Get latest news
    news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(3).all()
    
    # Get upcoming events
    events = Event.query.filter(Event.event_date >= datetime.utcnow()).order_by(Event.event_date.asc()).limit(3).all()
    
    # Get latest job postings
    latest_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(3).all()
    
    jobs_count = Job.query.count()
    
    total_hosted_events = Event.query.filter(Event.event_date < datetime.now(timezone.utc)).count()
    
    total_active_users = User.query.filter_by(is_active=True).count()
    stats = {
        'total_alumni': total_active_users,
        'total_events': total_hosted_events,
        'total_jobs': jobs_count
    }
    
    return render_template('index.html', title='Home', news=news, events=events, stats=stats, latest_jobs=latest_jobs)
