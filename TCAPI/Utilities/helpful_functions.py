import datetime
from ..models import *

# Ping function for Users activity
def ping(active, _token):
    token = Token.objects.get(token=_token)
    user = User.objects.get(token=token)
    if active:
        user.last_active_date = datetime.now()
        user.is_active = True
        user.save()
        return "Active"
    else:
        user.is_active = False
        user.save()
        return "Inactive"