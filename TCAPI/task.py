from celery import shared_task
from .models import User, Token
from datetime import datetime, timezone
import time
from .Utilities.helpful_functions import find_time_difference

@shared_task(bind=True)
def check_users_are_active_no_wallet(self):
    adjusted_user = False
    for user in User.objects.all():
        print(f"Username: {user.username}, is_active: {user.is_active}")
        if user.is_active:
            # if user.has_wallet is False:
            current_datetime = datetime.now(timezone.utc)
            users_date = user.last_active_date
            if find_time_difference(current_datetime, users_date):
                adjusted_user = True
                user.is_active = False
                user.in_queue = False
                user.in_game = False
                user.save()
    if adjusted_user:
        return "Adjusted Users."
    else:
        return "No Users Adjusted."

# Look into this later
    # 'check-users-are-active-with-wallet': {
    #     'task': 'TCAPI.task.check_users_are_active_with_wallet',
    #     'schedule': crontab(minute='*/3'),
    #     # args: (2,)
    # }
# @shared_task(bind=True)
# def check_users_are_active_with_wallet(self):
#     adjusted_user = False
#     for user in User.objects.all():
#         if user.is_active:
#             if user.has_wallet:
#                 current_datetime = datetime.now(timezone.utc)
#                 users_date = user.last_active_date
#                 if find_time_difference(current_datetime, users_date):
#                     adjusted_user = True
#                     token = user.token 
#                     user.is_active = False
#                     user.in_queue = False
#                     user.in_game = False
#                     user.logged_in = False
#                     token.token = "null"
#                     user.save()       
#                     token.save()
#     if adjusted_user:
#         return "Adjusted Users"
#     else:
#         return "No Users Adjusted"

@shared_task(bind=True)
def start_time_limit_for_users_streaks(self, data):
    print(data)
    # Testing that the timers dont overlap with users
    # Get token from data and get user
    token = data['token']
    token1 = Token.objects.get(token=token)
    user = User.objects.get(token=token1)
    # Get user in_streak_time_value and set it to one or 2 save set value in function
    got_value = data['value']
    # enter while loop if user.streak_time_value == saved_set_value: continue
    # else exit loop
    count = 0

    while count != 60:
        if user.is_active_task_value == got_value:
            print(count)
            print(f"Users Value here: {user.is_active_task_value}")
            print(f"Got Value here: {got_value}")
            print(got_value)
            time.sleep(1)
            count+=1
        else:
            break
    