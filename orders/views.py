from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Item, Order


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm


    def form_valid(self, form):
        cart = Cart(self.request)
        if cart and not self.request.user.is_anonymous:
            form.instance.user = self.request.user
            order = form.save()
            for item in cart:
                Item.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            self.request.session['order_id'] = order.id
            return redirect(reverse('payments:process'))
        messages.warning(self.request, 'Você não está logado!!')
        return redirect(reverse('orders:create'))
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


class OrderListView(ListView):
    def get_template_names(self):
        return 'orders/order_user.html'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


def order_detail(request, pk):
    order = Order.objects.filter(pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})