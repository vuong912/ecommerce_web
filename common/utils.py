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

class SQLUtils:
    def __init__(self):
        self.where_query=[]
        self.query_params=[]
        self.order_query=[]

    def add_where(self, query, param=None):
        if isinstance(query, list):
            self.where_query.extend(query)
        else:
            self.where_query.append(query)
        if param:
            if isinstance(param, list):
                self.query_params.extend(param)
            else:
                self.query_params.append(param)
    
    def add_order(self, query):
        if query:
            if isinstance(query, list):
                self.order_query.extend(query)
            else:
                self.order_query.append(query)

    def get_where_clause(self):
        if self.where_query:
            return 'WHERE ' + ' AND '.join(self.where_query)
        return ''

    def get_params(self):
        return self.query_params

    def get_order_clause(self):
        if self.order_query:
            return 'ORDER BY ' + ' , '.join(self.order_query)
        return ''