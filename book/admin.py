from django.contrib import admin
from .models import Merchandise, Book
#from django.conf.urls import patterns, include, url
# from .forms import MerchandiseChangeAdminForm
# # Register your models here.
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

class StatusFilter(SimpleListFilter):
    title = _('Trạng thái')

    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (None, _('Tất cả')),
            ('pending', _('Đang chờ kiểm duyệt')),
            ('selling', _('Đang bán')),
            ('blocked', _('Đã bị khóa')),
            ('rejected', _('Đã bị từ chối')),
            ('stopping', _('Tạm dừng bán')),
            ('sold_out', _('Đã bán hết')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset.filter()
        elif self.value() == 'rejected':
            return queryset.filter(activated_date__isnull = True, blocked_date__isnull = False)
        elif self.value() == 'pending':
            return queryset.filter(activated_date__isnull = True, blocked_date__isnull = True)
        elif self.value() == 'blocked':
            return queryset.filter(activated_date__isnull = False, blocked_date__isnull = False)
        elif self.value() == 'sold_out':
            return queryset.filter(activated_date__isnull = False, blocked_date__isnull = True, quantity = 0)
        elif self.value() == 'stopping':
            return queryset.filter(activated_date__isnull = False, blocked_date__isnull = True, quantity__gt = 0, stopped_date__isnull = False)
        elif self.value() == 'selling':
            return queryset.filter(activated_date__isnull = False, blocked_date__isnull = True, stopped_date__isnull = True)


class MerchandiseAdmin(admin.ModelAdmin):
    model=Merchandise
    change_form_template = "admin/book.html"
    list_display = ('id', 'user', 'get_portfolio', 'get_product_name', 'get_product_status')
    list_filter = [StatusFilter] 
    def get_portfolio(self, obj):
        return obj.portfolio.name
    get_portfolio.short_description = 'Loại sản phẩm'
    get_portfolio.admin_order_field = 'portfolio__name'

    def get_product(self, obj):
        product = Book.objects.get(pk=obj.id_product)
        return product
    get_product.short_description = 'Sản phẩm'

    def get_product_name(self, obj):
        product = Book.objects.get(pk=obj.id_product)
        return product.name
    get_product_name.short_description = 'Sản phẩm'
    #get_product_name.admin_order_field = 'get_product_name'

    def get_product_status(self, obj):
        return obj.get_merchandise_status()['name']
    get_product_status.short_description = 'Trạng thái'

    def response_change(self, request, obj):
        if "_make-unique" in request.POST:
            self.message_user(request, "Thay đổi đã được thực hiện.")
            return HttpResponseRedirect(".")
        
        return super().response_change(request, obj)
    

admin.site.register(Merchandise, MerchandiseAdmin)
