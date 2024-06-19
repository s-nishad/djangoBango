from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
@login_required
def redirect_view(request):
    return redirect('home:home')


@login_required
def console_view(request):
    return render(request, 'home/home.html', )
