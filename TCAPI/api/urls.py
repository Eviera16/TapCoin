from django.urls import path
from .views import registration_view, get_user, logout_view, login_view, find_game, send_points, create_game, get_game_Id, guest_login


app_name = "user_api"
urlpatterns = [
    path('register', registration_view, name="register"),
    path('info', get_user, name="getUser"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('findGame', find_game, name="findGame"),
    path('sendPoints', send_points, name="sendPoints"),
    path('createGame', create_game, name="createGame"),
    path('getGID', get_game_Id, name="getGameId"),
    path('guestLogin', guest_login, name="guestLogin"),
]