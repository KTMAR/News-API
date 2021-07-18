
from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page
from news.views import *


urlpatterns = [
    # path('search/', contact, name='search'),
    path('', HomeNews.as_view(), name='home'),
    # path('search/', Search.as_view(), name='search'),
    path('about/', about, name='about'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ViewNews.as_view(), name='post'),
    path('category/<slug:cat_slug>/', NewsByCategories.as_view(), name='category'),

]


