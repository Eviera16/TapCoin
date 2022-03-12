from django.urls import path
from .views import registration_view, get_user, logout_view, login_view, send_points, create_game, guest_login, send_cb, check_in_game


app_name = "user_api"
urlpatterns = [
    path('register', registration_view, name="register"),
    path('info', get_user, name="getUser"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('sendPoints', send_points, name="sendPoints"),
    path('createGame', create_game, name="createGame"),
    path('guestLogin', guest_login, name="guestLogin"),
    path('sendCB', send_cb, name="sendCommentorBug"),
    path('check_in_game', check_in_game, name="check_in_game"),
]