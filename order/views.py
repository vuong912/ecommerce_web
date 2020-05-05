from django.shortcuts import render, get_object_or_404
from .models import Order, OrderStatus, DetailOrder
from django.core.paginator import Paginator

# Create your views here.
def get_order(request):
    order = Order.objects.raw('''
        select `order`.`id`, `order`.`created_date`, `book`.`name`, sum(`dt_o`.`total_price_after_discount`) `price`
        from `order` join `detail_order` `dt_o` join `merchandise` `m` join `book`
        where `order`.`id` = `dt_o`.`id_order` AND `dt_o`.`id_merchandise` = `m`.`id` AND `m`.`id_product` = `book`.`id`
            AND `order`.`id_user` = %s
        group by `order`.`created_date`
    ''', [str(request.user.id)])
    #print(order)
    paginator = Paginator(order, 5)
    page_number = request.GET.get('page')
    pager = paginator.get_page(page_number)
    page_navigator = []
    for i in range(max(1, pager.number - 2), pager.number):
        page_navigator.append(i)
    page_navigator.append(pager.number)
    for i in range(pager.number + 1, min(pager.number + 2, pager.paginator.num_pages) + 1):
        page_navigator.append(i)

    return render(request, 'order/order_list.html', {'pager':pager, 'page_navigator': page_navigator})

def order_detail(request, id_order):
    order = get_object_or_404(Order, pk=id_order)
    details = DetailOrder.objects.raw('''
        select `d_o`.`id`, `image`.`url`, `book`.`name`, `d_o`.`quantity`, `d_o`.`total_price_after_discount`
        from `detail_order` `d_o` join `merchandise` `m` join `book` join `merchandise_image` `m_img` join `image`
        where `d_o`.`id_merchandise` = `m`.`id` AND `book`.`id` = `m`.`id_product` AND `m`.`id` = `m_img`.`id_merchandise` 
            AND `m_img`.`id_image` = `image`.`id`
            AND `d_o`.`id_order` = %s
    ''',str(id_order))
    print(details)
    return render (request, 'order/order_detail.html', {'order':order, 'details':details})

def check_out(request):
    return render (request, 'order/check_out.html')
