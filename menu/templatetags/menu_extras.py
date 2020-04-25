from django import template
from users.models import User
register = template.Library()
@register.inclusion_tag('menu/menu.html')
def show_customer_menu(user):
    return {'menu':['Sách tiếng việt', 'Sách tiếng anh'],'user':user}