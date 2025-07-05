from django.shortcuts import render, get_object_or_404
from .models import BusinessCard


def card_view(request, slug):
    card = get_object_or_404(BusinessCard, slug=slug)
    return render(request, 'bc/detail.html', {'card': card})
