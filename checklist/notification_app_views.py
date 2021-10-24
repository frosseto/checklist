
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from notifications.signals import notify


def msg_index(request):
    try:
        users = User.objects.all()
        user = User.objects.get(username=request.user)

        return render(request, 'checklist_notificacao.html', {'users': users, 'user': user, 'notifications': user.notifications.unread() })
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages.")


def message(request):
    try:
        if request.method == 'POST':
            sender = User.objects.get(username=request.user)
            receiver = User.objects.get(id=request.POST.get('user_id'))
            print(sender, receiver, request.POST.get('message'))
            notify.send(sender, recipient=receiver, verb='Message', description=request.POST.get('message'),
            cta_link='48')
            
            return redirect('/msg')
        else:
            return HttpResponse("Invalid request")
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages")