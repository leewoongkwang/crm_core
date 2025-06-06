# reports/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from reports.models import Report
from customers.models import Customer

@receiver(post_save, sender=Report)
def update_customer_report_flag_on_save(sender, instance, **kwargs):
    customer = instance.customer
    if not customer.has_report:
        customer.has_report = True
        customer.save(update_fields=["has_report"])

@receiver(post_delete, sender=Report)
def update_customer_report_flag_on_delete(sender, instance, **kwargs):
    customer = instance.customer
    has_others = Report.objects.filter(customer=customer).exists()
    if customer.has_report != has_others:
        customer.has_report = has_others
        customer.save(update_fields=["has_report"])
