from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',mainPage,name = 'main'),
    path('about',aboutPage,name = 'about'),
    path('request',requestPage,name = 'requset'),
    path('login',loginPage,name = 'login'),
    path('signup',signupPage,name = 'signup'),
    path('profile',viewProfile,name = 'profile'),
    path('profile/manage',manageProfile,name = 'manage_profile'),
    path('block',blockPage,name = 'block'),
    path('profile/manage/post/<int:pk>',managePost,name = 'manage'),
    path('join/<int:pk>',joinPost,name = 'join'),
    path('join/edit/<int:pk>',editComment,name = 'edit_cmt'),
    path('good/<int:gp>',goodPost,name = 'good_post'),
    path('goodcomment/<int:gc>/<int:id>',goodComment,name = 'good_comment'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)