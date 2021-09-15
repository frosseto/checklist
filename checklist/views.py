from django.shortcuts import render
from django import template
from django.contrib.auth.models import Group

register = template.Library()
@register.filter(name='has_group')


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def index(request):
    return render(request, 'index.html', {})

