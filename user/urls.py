from django.urls import path, include
from user.views import login_view, logout_view, signup_view, customer_details_view, update_customer_view, \
    delete_customer_view, update_user_view, update_customer_profile_view, my_profile_view, password_change_view, \
    my_profile_update_view

app_name = 'user'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('customer_details/<str:customer_guid>', customer_details_view, name='customer_details'),
    path('customer_info/update/<str:customer_guid>', update_customer_view, name='customer_update'),
    path('customer/user_info/update/<str:customer_guid>', update_user_view, name='user_update'),
    path('customer/update/<str:customer_guid>', update_customer_profile_view, name='customer_profile_update'),
    path('my_profile/', my_profile_view, name='my_profile'),
    path('my_profile/update/', my_profile_update_view, name='my_profile_update'),
    path('change_password/', password_change_view, name='password_change'),
    path('customer/delete/<str:customer_guid>', delete_customer_view, name='customer_delete'),
]
