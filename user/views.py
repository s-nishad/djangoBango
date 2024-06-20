from allauth.socialaccount.signals import social_account_added
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import render, redirect
from .models import Customer
from user.forms import LoginForm, CustomerSignUpForm, UserUpdateForm, CustomerUpdateForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                # send_user_logged_in.delay(user.id)
                login(request, user)
                return redirect('home:home')
        messages.error(request, 'Invalid credentials. Please try again.')
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context=context)


@receiver(social_account_added)
def social_account_added_callback(sender, **kwargs):
    request = kwargs.get('request')
    sociallogin = kwargs.get('sociallogin')
    if sociallogin:
        user = sociallogin.user
        user_id = user.id
        user_in_db = User.objects.get(id=user_id)
        user_in_db.username = user.email
        print(user_in_db.username)
        user_in_db.save()
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
                user=user,
                email=user.email,
            )
            customer.save()


def signup_view(request):
    form = CustomerSignUpForm()
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.email = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                Customer.objects.create(
                    user=user,
                    company=form.cleaned_data['company'],
                    contact=form.cleaned_data['contact'],
                    email=user.email
                )

                messages.success(request, 'Account created successfully!')
                return redirect('user:login')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {e}')
        else:
            form.add_error(None, 'Please correct the errors below.')

    context = {
        'form': form,
    }
    return render(request, 'user/create_customer.html', context=context)


@login_required
def customer_details_view(request, customer_guid):
    if request.user.is_staff:
        customer = Customer.objects.get(guid=customer_guid)

        context = {
            'customer': customer
        }
        return render(request, 'user/customer_details.html', context=context)


@login_required
def update_user_view(request, customer_guid):
    if request.user.is_staff:
        customer = Customer.objects.get(guid=customer_guid)
        user = customer.user

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=user)

            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.email = user_form.cleaned_data['username']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.save()

                messages.success(request, 'User details updated successfully!')
            else:
                error = user_form.errors
                messages.error(request, error)
                return redirect('user:customer_profile_update', customer_guid=customer.guid)
        return redirect('user:customer_details', customer.guid)


@login_required
def update_customer_view(request, customer_guid):
    if request.user.is_staff:
        customer = Customer.objects.get(guid=customer_guid)

        if request.method == 'POST':
            customer_form = CustomerUpdateForm(request.POST, instance=customer)

            if customer_form.is_valid():
                customer = customer_form.save(commit=False)
                customer.email = customer_form.cleaned_data['email']
                customer.save()

                messages.success(request, 'Customer details updated successfully!')

        return redirect('user:customer_details', customer.guid)


@login_required
def update_customer_profile_view(request, customer_guid):
    customer = Customer.objects.get(guid=customer_guid)
    user = customer.user

    customer_form = CustomerUpdateForm(instance=customer)
    user_form = UserUpdateForm(instance=user)

    context = {
        'customer_form': customer_form,
        'user_form': user_form,
        'customer': customer
    }

    return render(request, 'user/customer_update.html', context=context)


@login_required
def my_profile_view(request):
    if request.user.is_staff:
        context = {
            'user': request.user
        }
        return render(request, 'user/my_profile.html', context)
    else:
        user = request.user
        customer = Customer.objects.get(user=request.user)

        context = {
            'user': user,
            'customer': customer
        }
        return render(request, 'user/my_profile.html', context)


@login_required
def my_profile_update_view(request):
    if request.user.is_staff:
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        if request.method == 'POST':
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'User details updated successfully!')
                return redirect('user:my_profile')
        context = {
            'user_form': user_form,
        }

        return render(request, 'user/my_profile_update.html', context=context)

    elif request.user.is_authenticated:
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        try:
            customer = Customer.objects.get(user=request.user)
            customer_form = CustomerUpdateForm(request.POST or None, instance=customer)
        except Customer.DoesNotExist:
            customer_form = CustomerUpdateForm(request.POST or None)

        if request.method == 'POST':
            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()

                if customer_form.instance:
                    customer_form.save()
                else:
                    customer = Customer.objects.create(
                        user=request.user,
                        company=customer_form.cleaned_data['company'],
                        contact=customer_form.cleaned_data['contact']
                    )
                messages.success(request, 'User details updated successfully!')
                return redirect('user:my_profile')

        context = {
            'user_form': user_form,
            'customer_form': customer_form
        }

        return render(request, 'user/my_profile_update.html', context=context)


@login_required
def delete_customer_view(request, customer_guid):
    if request.user.is_staff:
        customer = Customer.objects.get(guid=customer_guid)
        customer.delete()

        messages.success(request, 'Customer deleted successfully!')
        return redirect('order:find_customer')


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user:my_profile')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'user/password_change.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('user:login')
