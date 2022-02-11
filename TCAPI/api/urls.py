from django.urls import path
from .views import registration_view, get_user, logout_view, login_view, find_game, send_points, create_game, get_game_Id, guest_login, send_cb, put_in_queue, take_out_queue, game_disconnect, leave_queue, check_game_status


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
    path('sendCB', send_cb, name="sendCommentorBug"),
    path('put_in_queue', put_in_queue, name="put_in_queue"),
    path('take_out_queue', take_out_queue, name="take_out_queue"),
    path('disconnected', game_disconnect, name="disconnect"),
    path('leaveQueue', leave_queue, name="leaveQueue"),
    path('check_game_status', check_game_status, name="checkGameStatus")
]