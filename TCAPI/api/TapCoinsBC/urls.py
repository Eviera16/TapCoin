from django.urls import path
from .views import save_wallet, pass_face_id


app_name = "tapcoinsbc_api"
urlpatterns = [
    path("saveWallet", save_wallet, name="saveWallet"),
    path("passFaceId",  pass_face_id, name="passFaceId"),
]