
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
  #  path('accounts', include('registration.backends.default.urls')),
    path("inventory/", include("Inventory.urls")),
    path("", auth_views.LoginView.as_view(template_name = "inventory_system/login.html"), name="login"), #Django login template
    path("logout/", auth_views.LogoutView.as_view(template_name = "inventory_system/logout.html"), name="logout")

]
