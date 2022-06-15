from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse
from localflavor.br.models import BRCPFField, BRPostalCodeField, BRStateField
from model_utils.models import TimeStampedModel

from pystore.models import Product


class Order(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE, default=1)
    cpf = BRCPFField('CPF')
    name = models.CharField('Nome Completo', max_length=250)
    email = models.EmailField()
    postal_code = BRPostalCodeField('CEP')
    address = models.CharField('Endereço', max_length=250)
    number = models.CharField('Número', max_length=250)
    complement = models.CharField('Complemento', max_length=250, blank=True)
    district = models.CharField('Bairro', max_length=250)
    state = BRStateField('Estado')
    city = models.CharField('Cidade', max_length=250)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Pedido {self.id}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_description(self):
        return ', '.join([f'{item.quantity}x {item.product.name}' for item in self.items.all()])

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'pk': self.pk})


class Item(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(settings.CART_ITEM_MAX_QUANTITY)
        ]
    )

    def get_total_price(self):
        return self.price*self.quantity

    def __str__(self):
        return str(self.id)