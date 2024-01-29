"""TCServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('tapcoinsapi/user/', include('TCAPI.api.User.urls', 'user_api')),
    path('tapcoinsapi/game/', include('TCAPI.api.Game.urls', 'game_api')),
    path('tapcoinsapi/friend/', include('TCAPI.api.Friend.urls', 'friend_api')),
    path('tapcoinsapi/tapcoinsbc/', include('TCAPI.api.TapCoinsBC.urls', 'tapcoinsbc_api')),
    path('tapcoinsapi/securityquestions/', include('TCAPI.api.SecurityQuestions.urls', 'securityquestions_api')),
]
