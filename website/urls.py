"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from citybae import views as map_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', map_views.search, name="search"),
    path('login/', map_views.login_view, name="login"),
    path('registration/', map_views.registration_view, name="registration"),
    path('rating/', map_views.rating_view, name="rating"),
    path('rating-overview/', map_views.rating_overview_view, name="rating-overview"),
    path('rating-detail/<int:pk>/', map_views.rating_detail_view, name="rating-detail"),
    path('success/', map_views.success_view, name="success"),
    path('failure/', map_views.failure_view, name="failure"),
    path('', include('django.contrib.auth.urls')),
    path("logout", LogoutView.as_view(next_page='/'), name="logout"),
    path('single-rating-detail/<int:pk>/', map_views.single_rating_detail_view, name="single-rating-detail"),
]
