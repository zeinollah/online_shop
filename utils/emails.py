from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings




def send_verification_email(user, token, subject="Verify your email address"):
    """
    Send verification email for user
    """
    verification_url = f"{settings.BASE_URL}/api/accounts/verify-email/{token.token}/"
    context = {
        "user": user.first_name ,
        "verification_url": verification_url,
        "expires_hours" : 24,
    }

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    text_content = render_to_string('emails/verification_email.txt', context)
    html_content = render_to_string('emails/verification_email.html', context)

    email = EmailMultiAlternatives(
        subject = subject,
        body = text_content,
        from_email = from_email,
        to = [to_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()



def send_order_confirmation_email(order, subject="Order Confirmation"):
    """
    Send order report email when order is paid
    """
    customer= order.customer.account
    context = {
        "customer_name": customer.first_name ,
        "order": order,
        "order_items": order.order_items.all(),
        "subtotal": sum(item.subtotal for item in order.order_items.all()),
        "total_discount": sum(item.discount for item in order.order_items.all()),
        "final_total": order.total_price,
    }

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = customer.email

    text_context = render_to_string("emails/order_confirmation.txt", context)
    html_context = render_to_string("emails/order_confirmation.html", context)

    email = EmailMultiAlternatives(
        subject = f"{subject} - {order.order_number}",
        body = text_context,
        from_email = from_email,
        to = [to_email],
    )
    email.attach_alternative(html_context, "text/html")
    email.send()