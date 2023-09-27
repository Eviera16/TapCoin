from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer, GetUserSerializer, LoginSerializer
from ..models import *
from decouple import config
import binascii
import os
import bcrypt
import requests
from random import randrange
import datetime
from datetime import timedelta
from django.utils.timezone import make_aware


queue_name = "A"
queue_A_count = 1
queue_B_count = 1
queue_C_count = 1
queue_D_count = 1

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            if type(user) == str:
                data["error"] = user
                data["isErr"] = True
                return Response(data)
            data['response'] = "succesfully registered a new user."
            data['username'] = user.username
            user1 = User.objects.get(username=data['username'])
            token = user1.token
            data['token'] = token.token
            user1.in_game = False
            user1.in_queue = False
            user1.logged_in = True
            if request.data['phone_number'] != "":
                user1.phone_number = request.data['phone_number']
                user1.has_phone_number = True
            user1.save()
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    data = {}
    if serializer.is_valid():
        user = serializer.save()
        if type(user) == dict:
            return Response(user)
        data['response'] = "Success"
        data['username'] = user.username
        user1 = User.objects.get(username=user.username)
        if user1.logged_in:
            newData = {
                'log_in_error': "User already logged in."
            }
            return Response(newData)
        user1.in_game = False
        user1.in_queue = False
        user1.logged_in = True
        user1.save()
        token = binascii.hexlify(os.urandom(config('TOKEN', cast=int))).decode()
        token1 = user1.token
        token1.token = token
        token1.save()
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
def get_user(request):
    newData = {
        "token": request.data['token']
    }
    
    serializer = GetUserSerializer(data=newData)

    data = {}

    if serializer.is_valid():
        user = serializer.save()
        data['response'] = "Getting your information"
        data['username'] = user.username
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        try:
            data['wins'] = user.wins
            data['losses'] = user.losses
            data['best_streak'] = user.best_streak
            data['win_streak'] = user.win_streak
        except:
            pass
        if type(user.friends) == list:
            data['friends'] = user.friends
        else:
            data['friends'] = ["0"]
        hasInvites = False
        invites = []
        for invite in GameInvite.objects.all():
            if invite.reciever == user.username:
                hasInvites = True
                invites.append(invite.sender)
        data['hasInvite'] = hasInvites
        data['invites'] = invites
        data['HPN'] = user.has_phone_number
        data['is_guest'] = user.is_guest
        if user.phone_number:
            data['phone_number'] = user.phone_number
        else:
            data['phone_number'] = "Phone number"
    else: 
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
def logout_view(request):
    session = request.data['token']
    
    data = {}

    token1 = None
    try:
        for token in Token.objects.all():
            if token.token == session:
                token1 = token
        data['response'] = "Success"
    except:
        data['response'] = "Failure"
        return Response(data)
    user = User.objects.get(token=token1)
    if user.is_guest:
        token1.delete()
        user.delete()
    else:
        user.logged_in = False
        user.in_queue = False
        user.in_game = False
        user.save()
        token1.token = "null"
        token1.save()
    return Response(data)

@api_view(['POST'])
def send_points(request):
    print("***** IN SEND POINTS *****")

    if request.data['type'] == "Custom":
        data = {
            "gameOver" : True
        }
        return Response(data)

    if request.data['winner'] == False:
        data = {
            "gameOver" : True
        }
        return Response(data)

    fPoints = request.data['fPoints']
    sPoints = request.data['sPoints']
    gameId = request.data['gameId']
    game = Game.objects.get(gameId=gameId)
    user1 = User.objects.get(username=game.first)
    user2 = User.objects.get(username=game.second)
    right_now = make_aware(datetime.datetime.now())
    
    if fPoints > sPoints:
        print("***** FPOINTS IS GREATER *****")
        user1.wins += 1

        if user1.streak_time:
            print("USER 1 HAS A STREAK TIME")
            time_limit = user1.streak_time + timedelta(minutes=2)
            if right_now < time_limit:
                print("STILL WITHIN THE TIME LIMITS")
                user1.win_streak += 1
            else:
                print("NOT WITHIN THE TIME LIMITS")
                user1.win_streak = 1
        else:
            print("NO STREAK TIME")
            user1.win_streak = 1 

        if user1.win_streak > user1.best_streak:
            print("NEW BEST STREAK")
            user1.best_streak = user1.win_streak

        user1.streak_time = right_now
        user1.save()
        user2.losses += 1
        if user2.win_streak > user2.best_streak:
            user2.best_streak = user2.win_streak
        user2.win_streak = 0
        user2.save()
        game.fPoints = fPoints
        game.sPoints = sPoints
        game.winner = user1.username
        game.winner_streak = user1.win_streak
        game.save()
    elif sPoints > fPoints:
        print("***** SPOINTS IS GREATER *****")
        user1.losses += 1
        if user1.win_streak > user1.best_streak:
            user1.best_streak = user1.win_streak
        user1.win_streak = 0
        user1.save()
        user2.wins += 1
        if user2.streak_time:
            print("USER 2 HAS A STREAK TIME")
            time_limit = user2.streak_time + timedelta(minutes=2)
            if right_now < time_limit:
                print("STILL WITHIN THE TIME LIMITS")
                user2.win_streak += 1
            else:
                print("NOT WITHIN TIME LIMITS")
                user2.win_streak = 1
        else:
            print("NO STREAK TIME")
            user2.win_streak = 1
        if user2.win_streak > user2.best_streak:
            print("NEW BEST STREAK")
            user2.best_streak = user2.win_streak
        user2.streak_time = right_now
        user2.save()
        game.fPoints = fPoints
        game.sPoints = sPoints
        game.winner = user2.username
        game.winner_streak = user2.win_streak
        game.save()
    else:
        print("***** IT IS A TIE *****")
        print("STOP")
        game.fPoints = fPoints
        game.sPoints = sPoints
        game.winner = "Tie"
        game.winner_streak = 0
        game.save()

    data = {
        "gameOver" : True
    }

    return Response(data)

@api_view(['POST'])
def create_game(request):
    
    token = Token.objects.get(token=request.data['token'])
    token1 = Token.objects.get(token=request.data['first'])
    token2 = Token.objects.get(token=request.data['second'])
    user = User.objects.get(token=token)
    user1 = User.objects.get(token=token1)
    user2 = User.objects.get(token=token2)

    data = {}

    if user.in_game == False:
        gameId = binascii.hexlify(os.urandom(8)).decode()
        Game.objects.create(first=user1.username, second=user2.username, gameId=gameId)
        user1.cg_Id = gameId
        user2.cg_Id = gameId
        user1.in_game = True
        user2.in_game = True
        user1.save()
        user2.save()
        data['gameId'] = gameId
        data['first'] = "True"
    else:
        data['gameId'] = user2.cg_Id
        data['first'] = "False"
        user1.in_game = False
        user2.in_game = False
        user1.save()
        user2.save()

    return Response(data)

@api_view(['POST'])
def guest_login(request):
    data = {}
    token = binascii.hexlify(os.urandom(config('TOKEN', cast=int))).decode()
    pw = "guestPassword"
    salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
    hashed = bcrypt.hashpw(pw.encode(config('ENCODE')), salt).decode()
    token1 = Token.objects.create(token=token)
    count = 0
    for user in User.objects.all():
        try:
            if user.username.split("_")[0] == "CoinTapper":
                count += 1
        except:
            count = count

    newCount = str(count)
    user = None
    try:
        user = User.objects.create(first_name="Guest",last_name="Tapper", username="CoinTapper_" + newCount, token=token1, password=hashed)
        user.is_guest = True
        user.in_game = False
        user.in_queue = False
        user.logged_in = True
        user.save()
        data['response'] = "succesfully registered a new guest user."
        data['username'] = user.username
        data['error'] = False
        data['token'] = token1.token
    except Exception as e:
        newError = str(e)
        newErr = newError.split("DETAIL:")[1]
        error = newErr.split("=")[1]
        data['response'] = "Something went wrong."
        data['username'] = error
        data['error'] = True
        data['token'] = ""
        return Response(data)

    return Response(data)

@api_view(['POST'])
def send_cb(request):
    tToken = request.data['token']
    token = Token.objects.get(token=tToken)
    user = User.objects.get(token=token)

    CommentOrBug.objects.create(message=request.data['text'], user=user.username)

    data={
        'response':'Successfully Sent'
    }

    return Response(data)

@api_view(['POST'])
def check_in_game(request):

    tk = request.data['token']
    token = Token.objects.get(token=tk)
    user = User.objects.get(token=token)
    data = {}
    if user.in_game:
        data['response'] = "INGAME"
    else:
        data['response'] = "OUTGAME"

    return Response(data)

@api_view(['POST'])
def send_friendRequest(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        user1 = User.objects.get(token=token1)
        user2 = User.objects.get(username=request.data['username'])
        if user1 == user2:
            data = {
                "result": "Cannot send request to self.",
                "friends": ["No friends"]
            }
            return Response(data)
        rString = "requested|"
        sString = "sentTo|"
        fRequest = rString + user1.username
        sRequest = sString + user2.username
        for friend in user1.friends:
            if sString in friend:
                if friend.split(sString)[1] == user2.username:
                    data = {
                        "result": "ALREADY SENT TO",
                        "friends": [user2.username]
                    }
                    return Response(data)
            elif rString in friend:
                if friend.split(rString)[1] == user2.username:
                    data = {
                        "result": "ALREADY RECIEVED",
                        "friends": [user2.username]
                    }
                    return Response(data)
        tempFriends1 = []
        tempFriends2 = []
        if type(user2.friends) == list:
            for name in user2.friends:
                if name != fRequest:
                    if name != sRequest:
                        tempFriends1.append(name)
        tempFriends1.append(fRequest)
        if type(user1.friends) == list:
            for name in user1.friends:
                if name != fRequest:
                    if name != sRequest:
                        tempFriends2.append(name)
        tempFriends2.append(sRequest)
        user1.friends = tempFriends2
        user2.friends = tempFriends1
        user1.save()
        user2.save()
        data = {
            "result": "Success",
            "friends": user1.friends
        }
        return Response(data)
    except:
        data = {
            "result": "Could not find username.",
            "friends": ["No friends"]
        }
        return Response(data)

@api_view(['POST'])
def accept_friendRequest(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        accepter = User.objects.get(token=token1)
        sender = User.objects.get(username=request.data['username'])
        rString = "requested|"
        sString = "sentTo|"
        newFriends = []
        for name in accepter.friends:
            if rString in name:
                newName = name.split("|")[1]
                if newName == sender.username:
                    newFriends.append(newName)
                else:
                    newFriends.append(name)
            else:
                newFriends.append(name)
        accepter.friends = newFriends
        accepter.save()
        newFriends2 = []
        for name in sender.friends:
            if sString in name:
                newName = name.split("|")[1]
                if newName == accepter.username:
                    newFriends2.append(newName)
                else:
                    newFriends2.append(name)
            else:
                newFriends2.append(name)
        sender.friends = newFriends2
        sender.save()
        data = {
            "result": "Accepted"
        }
        return Response(data)
    except:
        data = {
            "result": "Colud not accept request"
        }
        return Response(data)

@api_view(['POST'])
def decline_friendRequest(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        decliner = User.objects.get(token=token1)
        sender = User.objects.get(username=request.data['username'])
        rString = "requested|"
        sString = "sentTo|"
        newFriends = []
        for name in decliner.friends:
            if rString in name:
                newName = name.split("|")[1]
                if newName != sender.username:
                    newFriends.append(name)
            else:
                newFriends.append(name)
        decliner.friends = newFriends
        decliner.save()
        newFriends2 = []
        for name in sender.friends:
            if sString in name:
                newName = name.split("|")[1]
                if newName != decliner.username:
                    newFriends2.append(name)
            else:
                newFriends2.append(name)
        sender.friends = newFriends2
        sender.save()
        data = {
            "result": "Declined"
        }
        return Response(data)
    except:
        data = {
            "result": "Colud not decline request."
        }
        return Response(data)

@api_view(['POST'])
def remove_friend(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        remover = User.objects.get(token=token1)
        removed = User.objects.get(username=request.data['username'])
        newFriends = []
        for name in remover.friends:
            if name != removed.username:
                newFriends.append(name)
        remover.friends = newFriends
        remover.save()
        newFriends2 = []
        for name in removed.friends:
            if name != remover.username:
                newFriends2.append(name)
        removed.friends = newFriends2
        removed.save()
        data = {
            "result": "Removed"
        }
        return Response(data)
    except:
        data = {
            "result": "Could not remove friend."
        }
        return Response(data)

@api_view(['POST'])
def send_invite(request):
    token = Token.objects.get(token=request.data['token'])
    user1 = User.objects.get(token=token)
    user2 = User.objects.get(username=request.data['username'])
    gameId = binascii.hexlify(os.urandom(8)).decode()
    uniqueId = False
    while(not uniqueId):
        foundId = False
        for game in Game.objects.all():
            if game.gameId == gameId:
                foundId = True
                break
        if foundId:
            gameId = binascii.hexlify(os.urandom(8)).decode()
        else:
            uniqueId = True
    for gInvite in GameInvite.objects.all():
        if gInvite.sender == user1.username:
            if gInvite.reciever == user2.username:
                data = {
                    "first": "ALREADY EXISTS",
                    "second": "ALREADY EXISTS",
                    "gameId": "ALREADY EXISTS"
                }
                return Response(data)
        elif gInvite.sender == user2.username:
            if gInvite.reciever == user1.username:
                data = {
                    "first": "ALREADY EXISTS",
                    "second": "ALREADY EXISTS",
                    "gameId": "ALREADY EXISTS"
                }
                return Response(data)
    GameInvite.objects.create(sender=user1.username, reciever=user2.username, gameId=gameId)
    Game.objects.create(first=user1.username, second=user2.username, gameId=gameId)
    data = {
        "first":user1.username,
        "second":user2.username,
        "gameId":gameId
    }
    return Response(data)

@api_view(['POST'])
def ad_invite(request):
    sender = User.objects.get(username=request.data['username'])
    token = Token.objects.get(token=request.data['token'])
    reciever = User.objects.get(token=token)
    ad_request = request.data['adRequest']
    try:
        if ad_request == "delete":
            deleted = False
            try:
                if request.data['cancelled'] == True:
                    data = {
                        "result": "Cancelled"
                    }
                    return Response(data)
                else:
                    for invite in GameInvite.objects.all():
                        if invite.sender == sender.username:
                            if invite.reciever == reciever.username:
                                game = Game.objects.get(gameId=invite.gameId)
                                game.delete()
                                invite.delete()
                                deleted = True
                        elif invite.sender == reciever.username:
                            if invite.reciever == sender.username:
                                game = Game.objects.get(gameId=invite.gameId)
                                game.delete()
                                invite.delete()
                                deleted = True
                    if deleted:
                        data = {
                            "result": "Cancelled"
                        }
                    else:
                        data = {
                            "result": "Soemthing went wrong"
                        }
                    return Response(data)
            except:
                for invite in GameInvite.objects.all():
                    if invite.sender == sender.username:
                        if invite.reciever == reciever.username:
                            game = Game.objects.get(gameId=invite.gameId)
                            game.delete()
                            invite.delete()
                            deleted = True
                    elif invite.sender == reciever.username:
                        if invite.reciever == sender.username:
                            game = Game.objects.get(gameId=invite.gameId)
                            game.delete()
                            invite.delete()
                            deleted = True
                if deleted:
                    data = {
                        "result": "Cancelled"
                    }
                else:
                    data = {
                        "result": "Soemthing went wrong"
                    }
                return Response(data)
        else:
            game = None
            for invite in GameInvite.objects.all():
                if invite.sender == sender.username:
                    if invite.reciever == reciever.username:
                        game = Game.objects.get(gameId=invite.gameId)
                        invite.delete()
                        deleted = True
                elif invite.sender == reciever.username:
                    if invite.reciever == sender.username:
                        game = Game.objects.get(gameId=invite.gameId)
                        invite.delete()
                        deleted = True
            if deleted:
                data = {
                    "result": "Accepted",
                    "first":game.first,
                    "second":game.second,
                    "gameId":game.gameId
                }
            else:
                data = {
                    "result": "Soemthing went wrong"
                }
            return Response(data)
    except:
        data = {
            "result": "Somethiong went wrong"
        }
        return Response(data)

@api_view(['POST'])
def send_username(request):
    phone_number = request.data['phone_number']
    data = {
        "response": True,
        "message" : ""
    }

    try:
        user = User.objects.get(phone_number=phone_number)
        data['message'] = "BEFORE SEND TEXT"
        requests.post('https://textbelt.com/text', {
            'phone': phone_number,
            'message': f'Your username is: {user.username}',
            'key': '0d40a9c1f04d558428eb525db9b4502e0a15cd31F5JAs5vP0Yc2JcS2TzrtsqFKd',
        })
        data['message'] = "RESPONSE IS A SUCCESS"
    except Exception as e:
        data['response'] = False
        data['message'] = f"IN THE EXCEPT BLOCK e: {e}"
    
    return Response(data)

@api_view(['POST'])
def send_code(request):
    phone_number = request.data['phone_number']
    code = ""

    for i in range(4):
        num = randrange(10)
        code += str(num)
    data = {
        "response": True,
        "code" : code
    }

    try:
        user = User.objects.get(phone_number=phone_number)
        data['message'] = "BEFORE SEND TEXT"
        requests.post('https://textbelt.com/text', {
            'phone': phone_number,
            'message': f'Your temporary code is: {code}',
            'key': '951292afc50e335e0bc2ac92e70e3ecd4030853aQFJFjuPmMccnZjNCihpssKcII',
        })
        right_now = make_aware(datetime.datetime.now())
        user.p_code = int(code)
        user.p_code_time = right_now
        user.save()
        data['message'] = f"RESPONSE IS A SUCCESS {right_now}."
    except Exception as e:
        data['response'] = False
        data['message'] = f"IN THE EXCEPT BLOCK e: {e}"
    
    return Response(data)

@api_view(['POST'])
def change_password(request):
    if request.data['code'] == "SAVE":
        print("IN SAVED IF STATMENT")
        data = {
            "response": True,
            "message": "",
            "error_type": 0
        }
        try:
            print("IN THE TRY BLOCK")
            password = request.data['password']
            if password.strip() == "":
                data["response"] = False
                data["error_type"] = 0
                data["message"] = "Password can't be blank."
                return Response(data)
            print("AFTER CHECKING FOR EMPTY")
            token = Token.objects.get(token=request.data['token'])
            user = User.objects.get(token=token)
            print("GOT USER")
            newPW = bcrypt.hashpw(password.encode(config('ENCODE')), user.password.encode(config('ENCODE')))
            print("GOT NEW PW")
            if newPW == user.password.encode(config('ENCODE')):
                print("PASSWORD IS PREVIOUS PASSWORD")
                data["response"] = False
                data["error_type"] = 1
                data["message"] = "Password can't be previous password."
                print(data)
                return Response(data)
            print("PASSWORDS ARE DIFFERENT")
            salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
            print("GOT THE SALT")
            hashed = bcrypt.hashpw(password.encode(config('ENCODE')), salt).decode()
            print("GOT THE HASHED")
            user.password = hashed
            print("SET USER PASSWORD")
            user.is_guest = False
            print("SET THE GUEST")
            user.save()
            print("SAVED USER")
            data = {
                "response": True
            }
            print("SET THE DATA RESPONSE")
        except:
            print("IN EXCEPT BLOCK")
            data["response"] = False
            data["error_type"] = 3
            data["message"] = "Something went wrong."
        return Response(data)

    data = {
        "response": True,
        "expired": False,
        "message": "",
        "error_type": 0
    }
    code = request.data['code']
    password = request.data['password']
    if password.strip() == "":
        data["response"] = False
        data["error_type"] = 0
        data["message"] = "Password can't be blank."
        data["expired"] = False
        return Response(data)
    user = User.objects.get(p_code=int(code))
    ser_data = {
        "username": user.username,
        "password": password
    }
    newPW = bcrypt.hashpw(password.encode(config('ENCODE')), user.password.encode(config('ENCODE')))
    if newPW == user.password.encode(config('ENCODE')):
        data["response"] = False
        data["error_type"] = 1
        data["message"] = "Password can't be previous password."
        data["expired"] = False
        return Response(data)
    p_word_datetime_limit = user.p_code_time + timedelta(minutes=5)
    right_now = make_aware(datetime.datetime.now())
    try:
        if p_word_datetime_limit > right_now:
            salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
            hashed = bcrypt.hashpw(password.encode(config('ENCODE')), salt).decode()
            user.password = hashed
            user.save()
            data['message'] = f"Successfully saved password."
        else:
            data["response"] = False
            data['message'] = "Time limit reached. Invalid code."
            data["error_type"] = 2
            data['expired'] = True
    except:
        data['response'] = False
        data["error_type"] = 3
        data['message'] = "Something went wrong."
        data['expired'] = False

    return Response(data)
        
@api_view(['POST'])
def save(request):
    print("IN SAVE")
    data = {
        "response" : ""
    }

    try:
        print("IN TRY BLOCK")
        token = Token.objects.get(token=request.data['token'])
        print("CREATED TOKEN")
        user = User.objects.get(token=token)
        print("FOUND USER")
        for u in User.objects.all():
            if u.username == request.data['username']:
                if u != user:
                    print("INVALID USERNAME")
                    data['response'] = "Invalid username."
                    return Response(data)
        print("SAVING DATA")
        user.first_name = request.data['first_name']
        print("SAVED FIRST NAME")
        user.last_name = request.data['last_name']
        print("SAVED LAST NAME")
        user.username = request.data['username']
        print("SAVED USERNAME")
        user.phone_number = request.data['phone_number']
        print("SAVED PHONE NUMBER")
        user.save()
        print("SAVED")
        if request.data['guest']:
            print("IS A GUEST")
            data['response'] = "Guest"
        else:
            print("IS NOT A GUEST")
            data['response'] = "Successfully saved data."
    except Exception as e:
        print("E IS BELOW")
        print(e)
        data['response'] = "Something went wrong: " + e

    return Response(data)