from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user,token):
    send_email(
        '[Alumni Network] Reset Your Password',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
    )

def send_contact_notification(submission):
    send_email(
        f'New Contact Submission: {submission.subject}',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[current_app.config['ADMIN_EMAIL']],
        text_body=render_template('email/contact_notification.txt', submission=submission),
        html_body=render_template('email/contact_notification.html', submission=submission)
    )