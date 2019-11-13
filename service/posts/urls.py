
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from posts.views import post_detail,index,archived,home,contacts,unique

from accounts.views import(login_view,logout_view,register_view)


urlpatterns = [
    path('blog-detail/<id>',post_detail,name="index"),
    path('unique/<str:word>',unique,name="unique"),
    path('category/',index,name="index"),
    path('home/',home,name="home"),
    path('archived/',archived,name="archived"),
    path('contacts/',contacts,name="contacts"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
