from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart

# Create your views here.
@login_required
def get_cart(request):
     cart_items = Cart.objects.raw('''
          select `book`.`name`, `cart`.`quantity`, `m`.`id`, `m`.`price`, `image`.`url`
          from `cart` join `merchandise` `m` join `book` join `merchandise_image` `m_img` join `image`
          where `cart`.`id_merchandise` = `m`.`id` AND `m`.`id_product` = `book`.`id` AND `m_img`.`id_merchandise` = `m`.`id` 
               AND `image`.`id`= `m_img`.`id_image`
               AND `cart`.`id_user` = %s
          group by `cart`.`id`;
     ''',[str(request.user.id)])
     return render(request, 'cart/cart.html', {'cart_items':cart_items})