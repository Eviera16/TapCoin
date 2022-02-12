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
def find_game(request):
    data = {}

    if len(Queue.objects.all()) == 0:
        newArr = [request.data['token']]
        Queue.objects.create(queue=newArr)
    queue = Queue.objects.get(queueId=config('QUEUEID', cast=int))
    tempQueue = []
    for item in queue.queue:
        tk = Token.objects.get(token=item)
        user = User.objects.get(token=tk)
        if user.logged_in:
            if user.in_queue:
                if not user.in_create_game:
                    if not user.in_game:
                        tempQueue.append(item)
    queue.queue = tempQueue
    queue.save()
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
    token1 = Token.objects.get(token=request.data['first'])
    token2 = Token.objects.get(token=request.data['second'])
    t1 = token1.token
    t2 = token2.token
    user = User.objects.get(token=token)
    user1 = User.objects.get(token=token1)
    user2 = User.objects.get(token=token2)
    queue = Queue.objects.get(queueId=config('QUEUEID', cast=int))
    newQueue = []

    if not user1.in_create_game:
        user1.in_create_game = True
        user2.in_create_game = True
        user1.save()
        user2.save()
    elif not user2.in_create_game:
        user1.in_create_game = True
        user2.in_create_game = True
        user1.save()
        user2.save()

    data = {}

    if user.in_game:
        for item in queue.queue:
            if item != t1 and item != t2:
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
    game = Game.objects.get(gameId=user.cg_Id)
    first = game.first
    second = game.second
    data = {
        "gameId":user.cg_Id,
        "first":first,
        "second":second
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
def put_in_queue(request):

    tk = request.data['token']
    token = Token.objects.get(token=tk)
    user = User.objects.get(token=token)
    user.in_queue = True
    user.in_game = False
    user.in_create_game = False
    user.save()

    data = {
        "success" : "success"
    }

    return Response(data)

@api_view(['POST'])
def game_disconnect(request):

    game_id = request.data['gameId']

    dis_game = Game.objects.get(gameId=game_id)

    username_1 = dis_game.first
    username_2 = dis_game.second

    user_1 = User.objects.get(username=username_1)
    user_2 = User.objects.get(username=username_2)
    token_1 = user_1.token
    token_2 = user_2.token

    queue = Queue.objects.get(queueId=config('QUEUEID', cast=int))

    not_in_queue = (token_1.token, token_2.token)

    new_queue = []

    for token in queue.queue:
        if token not in not_in_queue:
            new_queue.append(token)

    queue.queue = new_queue
    queue.save()

    data = {
        "success":"success"
    }
    return Response(data)

@api_view(['POST'])
def leave_queue(request):

    tk = request.data['token']
    token = Token.objects.get(token=tk)
    user = User.objects.get(token=token)
    user.in_queue = False
    user.in_game = False
    user.save()
    queue = Queue.objects.get(queueId=config('QUEUEID', cast=int))
    new_queue = []
    for toke in queue.queue:
        if toke != token.token:
            new_queue.append(toke)

    queue.queue = new_queue
    queue.save()

    data = {
        "success": "success"
    }
    return Response(data)

@api_view(['POST'])
def check_game_status(request):

    check_game = Game.objects.get(gameId=request.data['gameId'])

    f_name = check_game.first
    s_name = check_game.second
    user1 = User.objects.get(username=f_name)
    user2 = User.objects.get(username=s_name)
    
    data = {}
    if user1.in_create_game:
        if user2.in_create_game:
            data['True'] = "True"
        else:
            data['False'] = "False"
    else:
        data['False'] = "False"

    return Response(data)