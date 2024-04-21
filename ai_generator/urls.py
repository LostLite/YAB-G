from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('blogs', views.all_blogs, name='blogs'),
    path('blogs/<int:id>', views.single_blog, name='single-blog'),
]