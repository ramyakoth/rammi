from django.contrib.auth.views import logout
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,{'template_name':'falcon_app/index.html'},name='index'),
    url(r'^logout',logout,{'next_page':'index'}, name='logout'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/drive', views.drive, name='drive'),
    url(r'^dashboard/upload', views.upload, name='jfu_upload'),
    url(r'^users', views.users, name='userlist'),
    url(r'^profile', views.profile, name='profile'),
    url( r'upload/', views.upload, name = 'jfu_upload' ),
    url(r'drive_storage/', views.drive_storage, name = 'drive_storage')
    ]
