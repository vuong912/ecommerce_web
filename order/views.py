from django.shortcuts import render, get_object_or_404
from .models import Order, OrderStatus, DetailOrder, HistoryOrderStatus
from cart.models import Cart
from users.models import Address
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import NewAddressForm

# Create your views here.
@login_required
def get_order(request):
    order = Order.objects.raw('''
        select `order`.`id`, `order`.`created_date`, `book`.`name`, sum(`dt_o`.`total_price_after_discount`) `price`
            , `stt`.`name` `status`, `stt`.`code` `status_code`
        from `order` join `detail_order` `dt_o` join `merchandise` `m` join `book` join `history_order_status` `h` join `order_status` `stt`
            join (select `id_order`, max(`created_date`) `max` from `history_order_status` group by `id_order`) as `tim_max_date`
        where `order`.`id` = `dt_o`.`id_order` AND `dt_o`.`id_merchandise` = `m`.`id` AND `m`.`id_product` = `book`.`id` AND `order`.`id` = `h`.`id_order`
            AND `h`.`id_order`=`tim_max_date`.`id_order` and `h`.`id_order_status` = `stt`.`id` and `h`.`created_date` = `tim_max_date`.`max`
            AND `order`.`id_user` = %s
        group by `order`.`id`
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

@login_required
def order_detail(request, id_order):
    order = get_object_or_404(Order, pk=id_order)
    details = DetailOrder.objects.raw('''
        select `d_o`.`id`, `image`.`url`, `book`.`name`, `d_o`.`quantity`, `d_o`.`total_price_after_discount` `price`, `book`.`id` `id_book`
        from `detail_order` `d_o` join `merchandise` `m` join `book` join `merchandise_image` `m_img` join `image`
        where `d_o`.`id_merchandise` = `m`.`id` AND `book`.`id` = `m`.`id_product` AND `m`.`id` = `m_img`.`id_merchandise` 
            AND `m_img`.`id_image` = `image`.`id`
            AND `d_o`.`id_order` = %s
    ''',str(id_order))
    # print(details)
    return render (request, 'order/order_detail.html', {'order':order, 'details':details})

@login_required
def check_out(request):
    #get cart item
    cart_items = Cart.objects.raw('''
          select `cart`.`id`, `book`.`name`, `cart`.`quantity`, `m`.`id` `merchandise_id`, `m`.`price`, `image`.`url`
          from `cart` join `merchandise` `m` join `book` join `merchandise_image` `m_img` join `image`
          where `cart`.`id_merchandise` = `m`.`id` AND `m`.`id_product` = `book`.`id` AND `m_img`.`id_merchandise` = `m`.`id` 
               AND `image`.`id`= `m_img`.`id_image`
               AND `cart`.`id_user` = %s
          group by `cart`.`id`;
     ''',[str(request.user.id)])
        #tính thành tiền
    sub_total = 0
    for i in cart_items:
        sub_total += i.price * i.quantity

    # form show
    form = NewAddressForm()
    # if request.method == 'POST':
    #     #lưu form nhập thông tin địa chỉ giao hàng mới
    #     form = NewAddressForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         #lưu đơn hàng
    #         # order = Order()
    #         # order.save()
    #         return redirect('order:order')

    # get user address
    address = Address.objects.filter(user_id=request.user.id)
    return render (request, 'order/check_out.html', {'form':form, 'cart':cart_items, 'sub_total':sub_total, 'address':address})

@login_required
def cancel_order(request, id_order):
    HistoryOrderStatus.objects.filter(order=id_order).update(order_status=4)
    return get_order(request)
