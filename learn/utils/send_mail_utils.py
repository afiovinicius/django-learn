import os
import threading
import logging
import resend

from dotenv import load_dotenv

from django.core import mail
from django.http import JsonResponse


load_dotenv()


def resend_send_mail(subject, message, tousers):
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        from_email = "hi@vicit.studio"

        data = {
            "from": from_email,
            "to": tousers,
            "subject": subject,
            "html": message,
        }

        email = resend.Emails.send(data)

        return email
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise e


def send_mail_thread(subject, message, fromuser, tousers):
    try:
        connection = mail.get_connection()
        connection.open()

        email = mail.EmailMessage(
            subject,
            message,
            fromuser,
            [tousers],
            connection=connection,
        )
        email.send()

        connection.close()
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")


def smtplib_send_mail(subject, message, fromuser, tousers):
    try:
        thread = threading.Thread(
            target=send_mail_thread, args=(subject, message, fromuser, tousers)
        )
        thread.start()
        return JsonResponse({"message": "Email enviado com sucesso!"})
    except Exception as e:
        print(f"Erro ao criar thread: {e}")
        raise e
