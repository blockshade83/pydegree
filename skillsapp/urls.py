from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/<str:keyword>', views.index, name='index'),
    path('register', views.register, name = 'register'),
    path('login', views.user_login, name = 'user_login'),
    path('logout', views.user_logout, name = 'user_logout'),
    path('add_posting', views.add_posting, name = 'add_posting'),
    path('view_posting/<int:posting_id>', views.view_posting, name = 'view_posting'),
    path('my_postings', views.my_postings, name = 'my_postings'),
    path('edit_posting/<int:posting_id>', views.edit_posting, name = 'edit_posting'),
    path('repost/<int:posting_id>/<str:return_to>', views.repost, name = 'repost'),
    path('deactivate_posting/<int:posting_id>/<str:return_to>', views.deactivate_posting, name = 'deactivate_posting'),
    path('update_org_details', views.update_org_details, name = 'update_org_details'),
]
