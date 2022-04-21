from django.urls import path

from . import views

urlpatterns = [
    path('', views.Get_Comment.as_view(), name='Get All Comments'),
    path('<uuid:user_id>/', views.Get_User_Comments.as_view(), name='Get Users Comments'),
    path('thread/<uuid:comment_id>/', views.Get_Comment_Thread.as_view(), name='Get Thread'),
    path('create/', views.Save_Comment.as_view(), name='Save Comment'),
    path('delete/', views.Delete_Comment.as_view(), name='Delete Comment'),
]