"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from polls import views
from polls import urls as questionnaire_urls  # Add this import
from vineland import urls as vineland_urls  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", views.index, name="index"),
    path('', include('polls.urls')),  # Ensure this line is present
    path('vineland/', include('vineland.urls')),
]
