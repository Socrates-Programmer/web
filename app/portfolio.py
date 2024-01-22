from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app
)
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('portfolio', __name__, url_prefix = '/')

@bp.route('/', methods = ['GET'])
def index():
    return render_template('portfolio/index.html')

@bp.route('/mail', methods = ['POST', 'GET'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_mail(name, email, message)
        return render_template('portfolio/sent_mail.html')        


def send_mail(name, email, message):
    mi_mail = 'marcosavila3006@gmail.com'
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])

    from_email = Email(mi_mail)
    to_mail = To(mi_mail, substitutions={
        "-name-": name,
        "-email-": email,
        "-message-": message,

    })

    html_content = """
        <p>Hola Marcos A, tienes un nuevo contacto desde la  Web:</p>
        <p>Nombre: -name-</p>
        <p>Correo: -email-</p>
        <p>Mensaje: -message-</p>
    """
    mail = Mail(mi_mail, to_mail, 'Nuevo contacto desde la web', html_content = html_content)

    response = sg.client.mail.send.post(request_body=mail.get())