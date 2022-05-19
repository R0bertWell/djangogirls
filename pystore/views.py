from random import randint
from typing import List
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from cart.forms import CartAddProductForm

class ProductDetailView(DetailView):
    queryset = Product.available.all()
    extra_context = {'form': CartAddProductForm()}

class ProductListView(ListView):
    category = None
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.available.all()

        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context
