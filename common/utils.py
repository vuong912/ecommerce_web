from ecommerce_web.settings import EMAIL_HOST_USER
from django.core.mail import send_mail as django_send_mail
import string
import random 

def send_mail(send_to, subject, message):
    django_send_mail(subject, message, EMAIL_HOST_USER, [send_to], fail_silently=False)

def send_mail_verification_code(send_to, code):
    send_mail(send_to, 
        'Xác thực email đăng ký tài khoản trên Chợ Sách', 
        'Link xác thực email: http://localhost:8000/user/verify/' + code)

def get_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))