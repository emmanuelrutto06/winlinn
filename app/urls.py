from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import re_path
from .views import AboutView, contacts, policy, frequentlyaskedquestions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),
    path('authentication/', include('authentication.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name='authenticate/profile.html'), name='user_profile'),
    path('about/', AboutView, name='about'),
    path('contact/', contacts, name='contacts'),
    path('frequently-asked-questions/', frequentlyaskedquestions, name='frequentlyaskedquestions'),
    path('policy/', policy, name='privacy-policy'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),
    path('', include('blog.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
