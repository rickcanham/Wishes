"""wishes_app URL Configuration

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

urlpatterns = [
    path('', views.disp_login),
    path('login',views.login),
    path('register',views.register),
    path('log_out',views.log_out),
    path('wishes',views.disp_home), 
    path('wishes/new',views.disp_new),  
    path('wishes/add',views.add_wish), 
    path('wishes/edit/<int:wish_id>',views.edit_wish),
    path('wishes/disp_edit/<int:wish_id>',views.disp_edit),
    path('wishes/remove/<int:wish_id>',views.remove_wish),
    path('wishes/grant/<int:wish_id>',views.grant_wish),
    path('wishes/like/<int:wish_id>',views.like_wish),
]