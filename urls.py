from django.urls import path
from estoreapp import views
from django.conf.urls.static import static
from estore import settings

urlpatterns = [
    path('index',views.index),
    path('productdetails/<pid>',views.pdetails),
    path('viewcart',views.viewcart),
    path('ulogin',views.ulogin),
    path('register',views.register),
    path('logout',views.ulogout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path("addtocart/<pid>",views.addtocart),
]

if settings.DEBUG:
    urlpatterns  += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)