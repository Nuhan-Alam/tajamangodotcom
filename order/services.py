from order.models import Cart, CartItem, OrderItem, Order
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from product.models import Product
from user.models import User

class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('product').all()

            total_price = sum([item.product.price *
                               item.quantity for item in cart_items])

            order = Order.objects.create(
                user_id=user_id, total_price=total_price)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity
                )
                for item in cart_items
            ]
            # [<OrderItem(1)>, <OrderItem(2)>]
            OrderItem.objects.bulk_create(order_items)

            cart.delete()

            return order

    @staticmethod
    def cancel_order(order, user):
        if user.is_staff:
            order.status = Order.CANCELED
            order.save()
            return order

        if order.user != user:
            raise PermissionDenied(
                {"detail": "You can only cancel your own order"})

        if order.status == Order.DELIVERED:
            raise ValidationError({"detail": "You can not cancel an order"})

        order.status = Order.CANCELED
        order.save()
        return order

    @staticmethod
    @transaction.atomic
    def add_to_cart(product: Product, user: User, quantity: int = 1):

        cart, created = Cart.objects.get_or_create(user=user)
        
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0}  
        )

        total_quantity = cart_item.quantity + quantity
        
        # Check stock availability
        if product.stock < total_quantity:
            raise Exception(f"Sorry, {product.name} is not available anymore at this moment.")
        

        cart_item.quantity = total_quantity
        cart_item.save()
        
        return cart_item
    
    @staticmethod
    @transaction.atomic
    def buy_now(product: Product, user: User, quantity: int = 1):
        """
        Create an immediate order for a single product
        """
        # Check stock availability
        if product.stock < quantity:
            raise Exception(f"Sorry, {product.name} is not available anymore at this moment.")
        
        total_amount = product.price * quantity
        
        # Create order
        order = Order.objects.create(
            user=user,
            total_price=total_amount,
        )
        
        # Create order item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
            total_price = product.price * quantity
            )
        
        # Reduce stock
        product.stock -= quantity
        product.save()
        
        return order