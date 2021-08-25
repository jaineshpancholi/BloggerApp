from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from blogapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name="home"),
    path('about/', About, name="about"),
    path('foods/', Foods, name="foods"),
    path('lifestyle/',Lifestyle, name="lifestyle"),
    path('contact/', Contact, name="contact"),
    path('login',Login, name="login"),
    path('logout/',Logout, name="logout"),
    path('signup/', Signup, name="signup"),
    path('blog_detail/<int:bid>/', BlogDetail, name="detail"),
    path('category_detail/<int:cid>/', categortyBlog, name="cateblog"),
    path('userpanel/', UserPanel, name="userpanel" ),
    path('blog_delete/<int:bid>/', DeleteBlog, name="delete"),
    path('addblog/', AddBlog, name="addblog"),
    path('edit_profile', Editprofile, name="editprofile"),
    path('change_password', Changepassword, name="changepassword"),
    path('like_blog/<int:bid>/', BlogLike, name="like"),
    path('comment_blog/<int:bid>/', BlogComment, name="comment"),

    ## eamil gateway ##

    path('gateway/', Gateway, name = "gateway"),
    path('email_gateway/', SendMail, name = "email"), 




]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
