import os
import jwt# used for encoding and decoding jwt tokens
from fastapi import HTTPException # used to handle error handling
from passlib.context import CryptContext # used for hashing the password 
from datetime import datetime, timedelta # used to handle expiry time for tokens

class Auth():

    secret = "moyinoluwaeremioluwasewew"
    def encode_token(self, id:str):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=50),
            'iat' : datetime.utcnow(),
        'scope': 'token',
            'sub' : id
        }
        return jwt.encode(
            payload, 
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'token'):
                return payload['sub']   
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
    


