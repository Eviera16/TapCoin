from rest_framework import serializers
from ..models import User, Token
import binascii
import os
import bcrypt
from decouple import config



class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=config('CHAR', cast=int))
    last_name = serializers.CharField(max_length=config('CHAR', cast=int))
    email = serializers.EmailField(max_length=config('CHAR', cast=int))
    username = serializers.CharField(max_length=config('CHAR', cast=int))
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def create(self, validated_data):
        token = binascii.hexlify(os.urandom(config('TOKEN', cast=int))).decode()
        pw = validated_data.pop("password")
        salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
        hashed = bcrypt.hashpw(pw.encode(config('ENCODE')), salt).decode()
        token1 = Token.objects.create(token=token)
        try:
            user = User.objects.create(**validated_data, token=token1, password=hashed)
        except Exception as e:
            newError = str(e)
            newErr = newError.split("DETAIL:")[1]
            error = newErr.split("=")[1]
            return error

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=config('CHAR', cast=int))
    password = serializers.CharField(max_length=config('CHAR', cast=int))

    def create(self, validated_data):
        user1 = None
        foundUser = False
        foundPassword = False
        try:
            for user in User.objects.all():
                if user.username == validated_data['username']: 
                    foundUser = True
                    newPW = bcrypt.hashpw(validated_data['password'].encode(config('ENCODE')), user.password.encode(config('ENCODE')))
                    if newPW == user.password.encode(config('ENCODE')):
                        foundPassword = True
                        user1 = user
            if foundUser == False:
                if foundPassword == False:
                    user1 = {
                        "error": True,
                        "user": "Could not find username.",
                        "password": "Incorrect Password."
                        }
            else:
                if foundPassword == False:
                    user1 = {
                        "error": True,
                        "user": "None",
                        "password": "Incorrect Password"
                    }
                
        except Exception as e:
            return False

        return user1

class GetUserSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=config('TK', cast=int))

    def create(self, validated_data):
        token1 = None
        user = None
        try:
            for token in Token.objects.all():
                if token.token == validated_data['token']:
                    token1 = token
            for user in User.objects.all():
                if user.token.token == token1.token:
                    user = user
                    break
        except:
            return False

        return user

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=config('TK', cast=int))

    def create(self, validated_data):
        token1 = None
        user = None
        try:
            for token in Token.objects.all():
                if token.token == validated_data['token']:

                    token1 = token
            for user in User.objects.all():
                if user.token == token1.id:
                    user = user
        except:
            return False
        token1.token = "null"
        token1.save()
        return user