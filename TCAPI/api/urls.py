from django.urls import path
from .views import registration_view, get_user, logout_view, login_view, find_game, send_points, create_game, get_game_Id, forgot_name, username_code, newUsername_code, forgot_password, new_password, guest_login


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
    path('forgotUsername', forgot_name, name="forgotName"),
    path('usernameCode', username_code, name="usernameCode"),
    path('newUsernameCode', newUsername_code, name="newUsernameCode"),
    path('forgotPassword', forgot_password, name="forgotPassword"),
    path('newPassword', new_password, name="newPassword"),
    path('guestLogin', guest_login, name="guestLogin"),
]