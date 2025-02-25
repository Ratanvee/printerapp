from django.urls import path
from .views import register, user_login, user_logout, dashboard, upload_document, home
from django.urls import path
# from .views import get_pending_orders, update_order_status
# from .views import dashboard, redirect_to_owner_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('dashboard/<int:user_id>/', dashboard, name='dashboard'),
    path('upload/<slug:unique_url>/', upload_document, name='upload_document'),
    # path('dashboard/', redirect_to_owner_dashboard, name='redirect_dashboard'),
    # path('dashboard/<str:username>/', dashboard, name='dashboard'),
    # path('orders/pending/', get_pending_orders, name='get_pending_orders'),
    # path('orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
]
