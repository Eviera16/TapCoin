from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer, GetUserSerializer, LogoutSerializer, LoginSerializer, GuestRegistrationSerializer
from ..models import *
import string
import secrets
from decouple import config
from django.shortcuts import redirect
import binascii
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import bcrypt
from django.core.mail import send_mail
from datetime import datetime  
import datetime
from datetime import timedelta 
import uuid


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
            data['email'] = user.email
            data['username'] = user.username
            user1 = User.objects.get(username=data['username'])
            token = user1.token
            data['token'] = token.token
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
        user1.in_game = False
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
        data['email'] = user.email
        try:
            data['wins'] = user.wins
            data['losses'] = user.losses
            data['best_streak'] = user.best_streak
            data['win_streak'] = user.win_streak
        except:
            pass
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
    token1.token = "null"
    token1.save()
    return Response(data)

@api_view(['POST'])
def find_game(request):
    data = {
        'response': "It's Working!!",
    }
    if len(Queue.objects.all()) == 0:
        newArr = [request.data['token']]
        Queue.objects.create(queue=newArr)
    queue = Queue.objects.get(queueId=config('QUEUEID', cast=int))
    inQueue = False
    for item in queue.queue:
        if item == request.data['token']:
            inQueue = True
    if inQueue == False:
        queue.queue.append(request.data['token'])
        queue.save()

    if len(queue.queue) > 1:
        firstInQueue = queue.queue[0]
        secondInQueue = queue.queue[1]

        if request.data['token'] == firstInQueue:
            data['first'] = request.data['token']
            data['second'] = secondInQueue
            data['response'] = "Found Queue"
        elif request.data['token'] == secondInQueue:
            data['second'] = request.data['token']
            data['first'] = firstInQueue
            data['response'] = "Found Queue"
        else:
            data['first'] = "None"
            data['second'] = "None"
            data['response'] = "Not yet"
    else:
        data['response'] = "Not yet"
    return Response(data)


@api_view(['POST'])
def send_points(request):

    fPoints = request.data['fPoints']
    sPoints = request.data['sPoints']
    gameId = request.data['gameId']
    game = Game.objects.get(gameId=gameId)
    user1 = User.objects.get(username=game.first)
    user2 = User.objects.get(username=game.second)
    
    if fPoints > sPoints:
        user1.wins += 1
        user1.win_streak += 1
        if user1.win_streak > user1.best_streak:
            user1.best_streak = user1.win_streak
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
    else:
        user1.losses += 1
        if user1.win_streak > user1.best_streak:
            user1.best_streak = user1.win_streak
        user1.win_streak = 0
        user1.save()
        user2.wins += 1
        user2.win_streak += 1
        if user2.win_streak > user2.best_streak:
            user2.best_streak = user2.win_streak
        user2.save()
        game.fPoints = fPoints
        game.sPoints = sPoints
        game.winner = user2.username
        game.winner_streak = user2.win_streak
        game.save()

    data = {
        "gameOver" : True
    }

    return Response(data)

@api_view(['POST'])
def create_game(request):

    token = Token.objects.get(token=request.data['token'])
    user = User.objects.get(token=token)
    user1 = User.objects.get(username=request.data['first'])
    user2 = User.objects.get(username=request.data['second'])
    t1 = user1.token
    t2 = user2.token
    token1 = t1.token
    token2 = t2.token
    queue = Queue.objects.get(queueId=config('QUEUEID', cast=int))
    newQueue = []

    data = {}

    if user.in_game:
        for item in queue.queue:
            if item != token1 and item != token2:
                newQueue.append(item)
        queue.queue = newQueue
        queue.save()
        data['gameId'] = user.cg_Id
        user1.in_game = False
        user2.in_game = False
        user1.save()
        user2.save()
    else:
        gameId = binascii.hexlify(os.urandom(config('GAMEID', cast=int))).decode()
        Game.objects.create(first=user1.username, second=user2.username, gameId=gameId)
        user1.cg_Id = gameId
        user2.cg_Id = gameId
        user1.in_game = True
        user2.in_game = True
        user1.save()
        user2.save()
        data['gameId'] = gameId

    return Response(data)

@api_view(['POST'])
def get_game_Id(request):
    token = request.data['token']
    uToken = Token.objects.get(token=token)
    user = User.objects.get(token=uToken)
    data = {
        "gameId":user.cg_Id
    }

    return Response(data)

@api_view(['POST'])
def forgot_name(request):
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(4))

    try:
        user = User.objects.get(email=request.data['email'])
    except:
        data = {
            "result" : "Error",
            "data" : "Invalid email."
        }
        return Response(data)
    for ecode in EmailCode.objects.all():
        if ecode.username == user.username:
            ecode.delete()
    EmailCode.objects.create(code=code, email=request.data['email'], username=user.username)
    send_mail(
        "Verification Code",
        f"Your verification code is {code}. You have 5 minutes before this code expires.",
        "thunderericviera@gmail.com",
        [request.data['email'],],
    )
    data = {
        "result": "Successfully sent email!"
    }
    return Response(data)


@api_view(['POST'])
def username_code(request):

    try:
        eCode = EmailCode.objects.get(code=request.data['code'])
    except:
        data = {
            "result": "Invalid code. Code does not exits."
        }
        return Response(data)

    plusFive = eCode.created_at + timedelta(minutes=5)
    eCode.inputCode = request.data['code']
    eCode.save()

    if eCode.updated_at > plusFive:
        eCode.delete()
        data = {
            "result" : "Success",
            "expired": True,
            "username": "Code has expired"
        }
        return Response(data)

    data = {
        "result": "Success",
        "expired": False,
        "username" : eCode.username
    }


    return Response(data)

@api_view(['POST'])
def newUsername_code(request):
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(4))
    user = User.objects.get(email=request.data['email'])
    EmailCode.objects.create(code=code, email=request.data['email'], username=user.username)
    send_mail(
        "Verification Code",
        f"Your verification code is {code}. You have 5 minutes before this code expires.",
        "thunderericviera@gmail.com",
        [request.data['email'],],
    )
    data = {
        "result": "Successfully sent email!",
        "expired": False
    }

    return Response(data)

@api_view(['POST'])
def forgot_password(request):

    if request.data['email'] == True:
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(4))
        try:
            user = User.objects.get(email=request.data['data'])
        except:
            data = {
                "result" : "Error",
                "data" : "Invalid email."
            }
            return Response(data)
        for ecode in EmailCode.objects.all():
            if ecode.username == user.username:
                ecode.delete()

        EmailCode.objects.create(code=code, email=request.data['data'], username=user.username)
        send_mail(
            "Verification Code",
            f"Your verification code is {code}. You have 5 minutes before this code expires.",
            "thunderericviera@gmail.com",
            [request.data['data'],],
        )
    else:
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(4))
        try:
            user = User.objects.get(username=request.data['data'])
        except:
            data = {
                "result" : "Error",
                "data" : "Invalid username."
            }
            return Response(data)

        for ecode in EmailCode.objects.all():
            if ecode.username == user.username:
                ecode.delete()

        EmailCode.objects.create(code=code, email=user.email, username=request.data['data'])
        send_mail(
            "Verification Code",
            f"Your verification code is {code}. You have 5 minutes before this code expires.",
            "thunderericviera@gmail.com",
            [user.email,],
        )

    data = {
        "result": "Success!",
        "email": user.email,
        "username": user.username
    }
        
    return Response(data)

@api_view(['POST'])
def new_password(request):
    user = User.objects.get(email=request.data['email'])

    newPW = request.data['password']
    salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
    hashed = bcrypt.hashpw(newPW.encode(config('ENCODE')), salt).decode()
    user.password = hashed
    user.save()

    data = {
        "result": "SUCCESS!"
    }

    return Response(data)

@api_view(['POST'])
def guest_login(request):
    data = {}
    token = binascii.hexlify(os.urandom(config('TOKEN', cast=int))).decode()
    pw = request.data['password']
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
        user = User.objects.create(first_name="Guest",last_name="Tapper",email="guestEmail" + newCount + "@gmail.com",username="CoinTapper_" + newCount, token=token1, password=hashed)
    except Exception as e:
        newError = str(e)
        newErr = newError.split("DETAIL:")[1]
        error = newErr.split("=")[1]
        data['error'] = True
        data['password'] = error
        return Response(data)
    data['response'] = "succesfully registered a new guest user."
    data['email'] = user.email
    data['username'] = user.username
    user1 = User.objects.get(username=data['username'])
    token = user1.token
    data['token'] = token.token
    return Response(data)
