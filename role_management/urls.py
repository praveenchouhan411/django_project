"""nathwani_erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('module/add/', views.create_module),
    path('module/get/', login_required(views.ModuleListView.as_view())),
    path('admin/create_user/', views.create_user),
    path('admin/user_list/', views.user_list),
    path('admin/create_user_type/', views.create_user_type, name='create_user_type'),
    path('admin/get_users_type/', views.user_type_list),
    path('module/edit/', views.edit_module),
    path('module/edit_user/', views.edit_user),
    path('module/edit_user_type/', views.edit_user_type),
    path('module/delete_module', views.delete_module),
    path('module/delete_user', views.delete_user),
    path('module/delete_user_type', views.delete_user_type),
    path('profile/', views.profile),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]

