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
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
queue_name = "A"
queue_A_count = 1
queue_B_count = 1
queue_C_count = 1
queue_D_count = 1

contract_abi_const = [{'inputs': [{'internalType': 'address', 'name': '_taptapCoinAddress', 'type': 'address'}, {'internalType': 'address', 'name': '_priceFeedAddress', 'type': 'address'}], 'stateMutability': 'nonpayable', 'type': 'constructor', 'name': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'previousOwner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'OwnershipTransferred', 'type': 'event'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'activePlayers', 'outputs': [{'internalType': 'address payable', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'addActivePlayer', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newAccount', 'type': 'address'}, {'internalType': 'string', 'name': 'code', 'type': 'string'}], 'name': 'addWallet', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'winner', 'type': 'address'}], 'name': 'awardTapTapCoin', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'winner', 'type': 'address'}, {'internalType': 'uint256', 'name': 'percentage', 'type': 'uint256'}], 'name': 'calculateWinnings', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'checkForUser', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'checkUserIsActive', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'checkUserPassedRECAPTCHA', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': 'str1', 'type': 'string'}, {'internalType': 'string', 'name': 'str2', 'type': 'string'}], 'name': 'compare', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'pure', 'type': 'function'}, {'inputs': [], 'name': 'getCurrentActualUsdOneCentCost', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getPrice', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getTotalTapTapCoinSupply', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}, {'internalType': 'uint256', 'name': 'dataIndex', 'type': 'uint256'}], 'name': 'getTransactionData', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'getUsersGamesCount', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'getUsersStreakCount', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'owner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}, {'internalType': 'string', 'name': 'code', 'type': 'string'}, {'internalType': 'uint256', 'name': 'transaction_price', 'type': 'uint256'}], 'name': 'passRECAPTCHA', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'playerIndexes', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address[]', 'name': 'users', 'type': 'address[]'}], 'name': 'removeActivePlayer', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'renounceOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'setUsersGamesTo100', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'streakBoard', 'outputs': [{'internalType': 'uint256', 'name': 'wins', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'games', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'waitTimeStart', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'passedRECAPTCHA', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isValidUser', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isValidRECAPTCHA', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isActive', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isWinner', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isAboveZero', 'type': 'bool'}, {'internalType': 'bool', 'name': 'has100Games', 'type': 'bool'}, {'internalType': 'bool', 'name': 'skipping', 'type': 'bool'}, {'components': [{'internalType': 'uint256', 'name': 'addWalletTransaction', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'recaptchaTransaction', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_1', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_2', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_3', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_4', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_5', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'totalTransactionAmount', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'hasTotalTransactions', 'type': 'bool'}], 'internalType': 'struct TapCoinGame.TotalTransactions', 'name': 'totalTransactions', 'type': 'tuple'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'taptapCoin', 'outputs': [{'internalType': 'contract IERC20', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'transferOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'winner', 'type': 'address'}, {'internalType': 'address', 'name': 'loser', 'type': 'address'}, {'internalType': 'uint256', 'name': 'transaction_price_winner', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_price_loser', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'isDevEnv', 'type': 'bool'}, {'internalType': 'uint256', 'name': 'percentage', 'type': 'uint256'}], 'name': 'updatePlayersWins', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'function'}]

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
    print("IN GET USER")
    newData = {
        "token": request.data['token']
    }
    print(newData)
    de_queue = request.data['de_queue']
    
    serializer = GetUserSerializer(data=newData)

    data = {}

    if serializer.is_valid():
        print("SERIALIZER VALID")
        user = serializer.save()
        data['response'] = "Getting your information"
        data['username'] = user.username
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        try:
            print("IN TRY BLOCK")
            data['wins'] = user.wins
            data['losses'] = user.losses
            data['best_streak'] = user.best_streak
            data['win_streak'] = user.win_streak
        except:
            print("IN EXCEPT BLOCK")
            pass
        if type(user.friends) == list:
            print("USER HAS FRIENDS")
            data['friends'] = user.friends
        else:
            print("USER HAS 0 FRIENDS")
            data['friends'] = ["0"]
        hasInvites = False
        invites = []
        for invite in GameInvite.objects.all():
            if invite.reciever == user.username:
                print("USER HAS INVITES")
                hasInvites = True
                invites.append(invite.sender)
        data['hasInvite'] = hasInvites
        data['invites'] = invites
        data['is_guest'] = user.is_guest
        if user.phone_number:
            print("USER HAS PHONE NUMBER")
            data['phone_number'] = user.phone_number
            user.has_phone_number = True
            data['HPN'] = True
            user.save()
        else:
            print("USER HAS NO PHONE NUMBER")
            data['phone_number'] = "No Phone number"
            data['HPN'] = False
    else: 
        print("SERIALIZER ERRORS")
        data = serializer.errors
    print("DATA BELOW")
    print(data)
    if de_queue:
        user.in_queue = False
        user.in_game = False
        user.save()
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

@api_view(['POST'])
def save_wallet(request):
    try:
        wallet_address = request.data['wallet']
        if wallet_address != "None":
            print("THE WALLET ADDRESS IS BELOW")
            print(wallet_address)
            # Load the contract ABI and address
            contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
            contract_abi = contract_abi_const
            print("SET THE CONTRACT ADDRRESS AND ABI")

            # Create a contract object
            contract = w3.eth.contract(address=contract_address, abi=contract_abi)
            print("CREATED THE CONTRACT VARIABLE")

            # Interact with the contract (e.g., call functions)
            result = contract.functions.addWallet("0xf879FA272A149906d5d85943De35f7dc383AdeD0", "TEMPORARYADDWALLETPASSCODE").call()
            print("RESULT IS BELOW")
            print(result)
            data = {
                "response": "SUCCESS"
            }
            return Response(data)
    except Exception as e:
        print("IN THE EXCEPT BLOCK")
        print(e)
        data = {
            "response": "Something went wrong."
        }
        return Response(data)