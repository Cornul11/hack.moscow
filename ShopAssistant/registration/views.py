from django.shortcuts import render, redirect
from database.models import Users, UsersInterests

def register(request):
    user = Users.objects.create(name=request.POST['name'], age=request.POST['age'], password=request.POST['password'],
                               email=request.POST['email'], gender=request.POST['gender'])
    user.save()
    for i in request.POST['interests']:
        inter = UsersInterests.objects.create(email=request.POST['email'], interest=i)
        inter.save()
    request.session['email'] = user.email
    return redirect('/success')


def login(request):
    error = ''
    if request.method == 'POST':
        if Users.objects.filter(email=request.POST['email']).exists():
            user = Users.objects.filter(email=request.POST['email'])[0]
            if request.POST['password'] == user.password:
                request.session['email'] = user.email
                redirect('/success')
            else:
                error = u'Неверно введен пароль. Попробуйте снова.'
                context = {
                    "error": error
                }
        else:
            error = u'Такого логина не существует. Зарегистрируйтесь.'
            context = {
                "error": error
            }
        return render(request, 'login.html', context)

