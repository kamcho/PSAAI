from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, MyProfile, Home, LoginRedirect, FinishSetup, Login
from django.contrib.sitemaps.views import sitemap

urlpatterns = [

    path('Sign-Up/', RegisterView.as_view(), name='register'),
    path('Profile/', MyProfile.as_view(), name='profile'),
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps},name="django.contrib.sitemaps.views.sitemap",)
    path('', Home.as_view(), name='student-home'),
    path('login-Redirect/', LoginRedirect.as_view(), name='redirect'),
    path('Profile-Set-Up/', FinishSetup.as_view(), name='edit-profile'),
    path('Sign-In/', Login.as_view(), name='login'),
    path('Logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),

]
