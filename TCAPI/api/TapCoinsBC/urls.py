from django.urls import path
from .views import save_wallet, pass_face_id, award_tap_coin


app_name = "tapcoinsbc_api"
urlpatterns = [
    path("saveWallet", save_wallet, name="saveWallet"),
    path("passFaceId",  pass_face_id, name="passFaceId"),
    path("award_tap_coin", award_tap_coin, name="awardTapCoin")
]