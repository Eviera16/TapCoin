from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer, GetUserSerializer, LoginSerializer
from ..models import *
from decouple import config
import binascii
import os
import bcrypt



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

    fPoints = request.data['fPoints']
    sPoints = request.data['sPoints']
    gameId = request.data['gameId']
    game = Game.objects.get(gameId=gameId)
    user1 = User.objects.get(username=game.first)
    user2 = User.objects.get(username=game.second)
    
    if fPoints > sPoints:
        print("***** FPOINTS IS GREATER *****")
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
    elif sPoints > fPoints:
        print("***** SPOINTS IS GREATER *****")
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
        user = User.objects.create(first_name="Guest",last_name="Tapper", username="CoinTapper_" + newCount, token=token1, password=hashed)
    except Exception as e:
        newError = str(e)
        newErr = newError.split("DETAIL:")[1]
        error = newErr.split("=")[1]
        data['error'] = True
        data['password'] = error
        return Response(data)
    data['response'] = "succesfully registered a new guest user."
    data['username'] = user.username
    user1 = User.objects.get(username=data['username'])
    token = user1.token
    data['token'] = token.token
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
