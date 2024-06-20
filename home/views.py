from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user.models import Customer


# Create your views here.
@login_required
def redirect_view(request):
    return redirect('home:home')


@login_required
def console_view(request):
    user = request.user
    user.username = user.email
    print(user.username)
    user.save()
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            email=request.user.email,
        )
        customer.save()
    return render(request, 'home/home.html', )
