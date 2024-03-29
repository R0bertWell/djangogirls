from django.contrib import admin

from .models import Item, Order
from payments.models import Payment

class ItemInline(admin.TabularInline):
    model = Item
    raw_id_fields = ['product']
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    can_delete = False
    readonly_field = (
        'email', 
        'doc_number', 
        'transaction_amount',
        'installments', 
        'payment_method_id', 
        'mercado_pago_id', 
        'mercado_pago_status', 
        'mercado_pago_status_detail', 
        'modified',
    )

    ordering = ('-modified',)

    def has_add_permission(self, request, obj):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'name', 'email', 'cpf', 'paid', 'created', 'modified']
    list_filter = ['paid', 'created', 'modified']
    search_fields = ['name', 'email', 'cpf']
    inlines = [ItemInline, PaymentInline]