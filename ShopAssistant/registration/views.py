from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect

from database.models import Users, UsersInterests, Interests


def register(request):
    user = Users.objects.create(name=request.POST['name'], email=request.POST['email'],
                                age=request.POST['age'],
                                gender=request.POST['gender'], password=request.POST['password'])
    user.save()
    request.session['email'] = user.email
    s = SessionStore()
    s['email'] = user.email
    s.create()
    return render(request, 'interests.html')


def interests(request):
    user = Users.objects.filter(email=request.session['email']).first()
    for i in request.POST.getlist('interests'):
        interest = Interests.objects.filter(name=i).first()
        inter = UsersInterests(email=user, interest=interest)
        inter.save()
    return redirect('/success')


def index(request):
    return render(request, 'signup.html')

def gologin(request):
    return render(request, 'login.html')


def gosignup(request):
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        if Users.objects.filter(email=request.POST['email']).exists():
            user = Users.objects.filter(email=request.POST['email'])[0]
            if request.POST['password'] == user.password:
                request.session['email'] = user.email
                s = SessionStore()
                s['email'] = user.email
                s.create()
                return redirect('/success')

        return render(request, 'login.html')


def success(request):
    user = Users.objects.get(email=request.session['email'])
    context = {
        "user": user
    }
    return render(request, 'success.html', context)

