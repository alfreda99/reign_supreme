import traceback

from flask import Blueprint, render_template, send_from_directory, request
from flask import jsonify, make_response, abort


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import json

home = Blueprint('home', __name__)

@home.route('/test')
def test():
    return "Hello, World!"


# special file handlers and error handlers
@home.route('/favicon.ico')
def favicon():
    #home root path =/vagrant/reign_supreme/ww_app/static/components/home
    #app root path = /vagrant/reign_supreme/ww_app

    print("************************************** home.root_path")
    print(app.root_path)
    return send_from_directory(app.root_path+'/../../img/','favicon.ico')


@home.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html')


@home.route('/api/notification/intro', methods=['POST'])
def notify_intro():
    print('##########################::/api/notification/intro:: starting ##########################')

    fullname = request.form['fullname']
    email = request.form['email']
    message = request.form['message']

    sendto_email ="info@findyourbluesky.com"
    subject = "ReignSupreme Contact Notification"
    email_msg = "You have received a new message from ReignSupreme contact form.\n\n.Here are the details:\n\n Name: {0}\n\nEmail: {1}\n\nMessage:\n{2}".format(fullname, email, message)
    print(email_msg)
    try:

        app_notify(fullname, sendto_email, subject, email_msg)
        response = {'resultStatus': 'success'}

    except Exception:
        print("notify_intro():: Failed to send intro notification:  {0}".format(email))
        traceback.print_exc()
        response = {'resultStatus': 'error', 'errorMessage': 'Failed to send intro notification.'}

    return jsonify(response)


def app_notify(name, email, subject, message):
    fromaddr = 'support@lienloft.com'
    toaddr = email

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr

    # attach the body with the msg instance
    msg.attach(MIMEText(message, 'plain'))
    content = msg.as_string()

    # Send download via smtp
    username = 'support@lienloft.com'
    password = 'free@Last99'
    mailserver = smtplib.SMTP_SSL('smtp.mail.us-west-2.awsapps.com', 465)
    mailserver.login(username, password)
    mailserver.sendmail(fromaddr, toaddr, content)
    mailserver.quit()

