from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import send_mail
from order.models import Order

@receiver(post_save, sender=Order)
def order_confirmation_email(sender, instance, created, **kwargs):
    """Send order confirmation email when a new order is created"""
    if created:
        order = instance
        user = order.user  # Get the user from the order
        
        subject = f"Order Confirmation - Order #{str(order.id)[:8]}"
        
        # Create a proper message string
        message = f"""Hi {user.first_name},

Your order has been confirmed!

Order Details:
- Order ID: {str(order.id)}
- Total Amount: ${order.total_price}
- Status: {order.status}
- Created: {order.created_at.strftime('%B %d, %Y at %I:%M %p')}

Items Ordered:"""     
        # Add order items to the message
        for item in order.items.all():
            message += f"\n- {item.quantity} x {item.product.name} @ ${item.price} each" 
        message += f"""

Thank you for your order!

Best regards,
TajaMangoDotCom """

        recipient_list = [user.email]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False
            )
            print(f"Order confirmation email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send email to {user.email}: {str(e)}")








    if not created and instance.status == 'Delivered':
        order = instance
        user = order.user
        
        subject = f"Order Delivered - Order #{str(order.id)[:8]}"
        
        message = f"""Hi {user.first_name},

Congratulation!Your order has been delivered.

Order Details:
- Order ID: {str(order.id)[:8]}
- Total Amount: ${order.total_price}
- Delivered on: {order.updated_at.strftime('%B %d, %Y at %I:%M %p')}

Thank you for shopping with us!

Best regards,
Your Store Team"""

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )
            print(f"Order completion email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send completion email to {user.email}: {str(e)}")