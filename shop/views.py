from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Product, Order, OrderItem
from .forms import RegisterForm, CheckoutForm


def home(request):

    products = Product.objects.all()

    return render(
        request,
        "home.html",
        {
            "products": products
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        "product_detail.html",
        {
            "product": product
        }
    )


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session["cart"] = cart

    messages.success(
        request,
        "Product added to cart!"
    )

    return redirect("cart")


def cart(request):

    cart = request.session.get(
        "cart",
        {}
    )

    items = []

    total = Decimal("0")

    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            }
        )

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total
        }
    )


def remove_from_cart(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


def register(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


@login_required
def checkout(request):

    cart = request.session.get(
        "cart",
        {}
    )

    if not cart:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("home")

    items = []

    total = Decimal("0")

    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            }
        )

    if request.method == "POST":

        form = CheckoutForm(
            request.POST
        )

        if form.is_valid():

            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                address=form.cleaned_data["address"],
                phone=form.cleaned_data["phone"]
            )

            for item in items:

                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price
                )

            request.session["cart"] = {}

            messages.success(
                request,
                "Order placed successfully!"
            )

            return redirect("orders")

    else:

        form = CheckoutForm()

    return render(
        request,
        "checkout.html",
        {
            "form": form,
            "items": items,
            "total": total
        }
    )


@login_required
def orders(request):

    orders = Order.objects.filter(
        user=request.user
    )

    return render(
        request,
        "orders.html",
        {
            "orders": orders
        }
    )