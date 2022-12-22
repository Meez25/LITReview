"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


import critics.views
import authentication.views

urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    # path("flux/", critics.views.flux, name="flux"),
    path("flux/", critics.views.flux, name="flux"),
    path("posts/", critics.views.my_posts, name="my_posts"),
    path("posts/<int:ticket_id>/modify", critics.views.modify_post, name="modify_post"),
    path("posts/<int:ticket_id>/delete", critics.views.delete_post, name="delete_post"),
    path("abonnement", critics.views.abonnement, name="abonnement"),
    path("admin/", admin.site.urls),
    path("signup/", authentication.views.signup_page, name="signup"),
    path(
        "createticket/",
        critics.views.TicketCreateView.as_view(),
        name="create_ticket",
    ),
    path(
        "createreview/",
        critics.views.create_review,
        name="create_review",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
