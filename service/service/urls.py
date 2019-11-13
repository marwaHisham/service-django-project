"""service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static

from accounts.views import(login_view,logout_view,register_view)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^posts/',include("posts.urls"),name="posts"),
    url(r'^comments/',include("comments.urls"),name="comments"),
    url(r'^login/',login_view,name="login"),
    url(r'^register/',register_view,name="register"),
    url(r'^logout/',logout_view,name="logout"),
   # url(r'^ajax_is_favorite/$', ajax_is_favorite, name='ajax_is_favorite'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
