from django import template

register = template.Library()
@register.inclusion_tag('menu/menu.html')
def show_customer_menu():
    return {'menu':['Sách tiếng việt', 'Sách tiếng anh']}