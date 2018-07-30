"""proj1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from django.urls import path
from app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/', views.base),
    #url(r'^register/', views.register),
    url(r'^register/', views.validations_register),
    #url(r'^login/', views.login),
    url(r'^login/', views.afterlogin),
    url(r'^student_dashboard/', views.studentdash),
    url(r'^librarian_dashboard/', views.librariandash),
    url(r'^logout/', views.logout),
    url(r'^book-details/', views.book_details),
     url(r'^student_profile/', views.student_profile),
     url(r'^search/', views.search),
     url(r'^$', views.abcd),
     url(r'^status/',views.status),
     url(r'^PickedUp/',views.pickedup),
     url(r'^Returned/',views.returned),
     url(r'^issued_books/',views.issued_books),
     url(r'^returned_books/',views.returned_books),
     url(r'^pdf/',views.gen_pdf),
     #url(r'^byauthor/', views.byauthor),
     #url(r'^bysubject/', views.bysubject),
]
