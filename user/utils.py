from django.core.mail import EmailMessage
from .models import MyUser

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()



 
def get_username(user_name):
    try   :
        username = MyUser.objects.get(email=user_name).username
    except:
        username = user_name
    return username



