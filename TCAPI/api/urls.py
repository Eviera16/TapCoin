from django.urls import path
from .views import registration_view, get_user, logout_view, login_view, send_points, create_game, guest_login, send_cb, check_in_game, send_friendRequest, accept_friendRequest, decline_friendRequest, remove_friend, send_invite, ad_invite, send_username


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
    path('sfr', send_friendRequest, name="sendFriendRequest"),
    path("afr", accept_friendRequest, name="acceptFriendRequest"),
    path("dfr", decline_friendRequest, name="declineFriendRequest"),
    path("remove_friend", remove_friend, name="removeFriend"),
    path("send_invite", send_invite, name="sendInvite"),
    path("ad_invite", ad_invite, name="accept/declineInvite"),
    path("send_username", send_username, name="sendUsername")
]