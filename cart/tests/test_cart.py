import pytest
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from pystore.tests.factories import ProductFactory

from ..cart import Cart

pytestmark = pytest.mark.django_db


def dummy_get_response(request):
    return None


@pytest.fixture
def http_request():
    request = HttpRequest()
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(request)
    return request


@pytest.fixture
def session(http_request):
    return http_request.session


@pytest.fixture
def cart(http_request, session):
    cart = Cart(http_request)
    session.modified = False
    return cart


def test_create_empty_cart(http_request, session):
    assert session.get('cart') is None
    Cart(http_request)
    assert session['cart'] == {}


def test_create_empty_cart_2():
    request = HttpRequest()
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(request)

    assert request.session.get('cart') is None
    Cart(request)
    assert request.session['cart'] == {}


def test_create_empty_cart(http_request, session):
    session['cart'] = {'1':{}}
    Cart(http_request)
    assert session['cart'] == {'1':{}}


def test_create_empty_cart_2():
    request = HttpRequest()
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(request)

    request.session['cart'] = {'1':{}}
    Cart(request)
    assert request.session['cart'] == {'1':{}}


def test_add_product_to_empty_car(product, cart, session):
    cart.add(product)

    assert session['cart'] == {
        str(product.id): {'quantity': 1, 'price': str(product.price)}
    }
    assert session.modified


def test_add_product_to_empty_car_quantity_gt_1(product, cart, session):
    cart.add(product, 2)

    assert session['cart'] == {
        str(product.id): {'quantity': 2, 'price': str(product.price)}
    }
    assert session.modified


def test_add_product_to_empty_cart_twice(product, cart, session):
    cart.add(product)

    cart.add(product, 2)

    assert session['cart'] == {
        str(product.id): {'quantity': 3, 'price': str(product.price)}
    }
    assert session.modified


def test_add_product_to_empty_cart_override_quantity(product, cart, session):
    cart.add(product)

    cart.add(product, 4, override_quantity=True)

    assert session['cart'] == {
        str(product.id): {'quantity': 4, 'price': str(product.price)}
    }

    assert session.modified


def test_remove_product(product, cart, session):
    cart.add(product)

    cart.remove(product)
    assert session['cart'] == {}
    assert session.modified


def test_remove_product_not_in_cart(product, cart, session):
    cart.remove(product)

    assert session['cart'] == {}
    assert not session.modified


def test_iter_cart(cart, session):
    p1 = ProductFactory()
    p2 = ProductFactory()
    p3 = ProductFactory()

    cart.add(p1)
    cart.add(p2, 2)
    cart.add(p3, 3)
    session.modified = False

    products = [p1, p2, p3]
    quantities = [1, 2, 3]

    for product, quantity, item in zip(products, quantities, cart):
        assert product.price == item['price']
        assert product.price * quantity == item['total_price']
        assert product == item['product']

    assert not session.modified
    assert list(cart.cart.values()) != list(iter(cart))


def test_cart_length(cart):
    p1 = ProductFactory()
    p2 = ProductFactory()

    assert len(cart) == 0

    cart.add(p1)
    assert len(cart) == 1

    cart.add(p2, 3)
    assert len(cart) == 4

    cart.remove(p2)
    assert len(cart) == 1

    cart.remove(p1)
    assert len(cart) == 0


def test_get_total_price(cart):
    p1 = ProductFactory()
    p2 = ProductFactory()

    cart.add(p1)
    cart.add(p2, 2)

    total_price = (p1.price * 1) + (p2.price * 2)

    assert cart.get_total_price() == total_price
