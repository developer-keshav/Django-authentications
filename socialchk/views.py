
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    print(request)
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render(request, 'socialchk/home.html')

def login(request):
    return render(request, 'socialchk/login.html')
