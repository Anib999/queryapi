# from passlib.context import CryptContext
from passlib.hash import bcrypt

# pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hashpassword(password: str):
    hashed_password = bcrypt.using(rounds=12).hash(password)
    return hashed_password

def verifyhashpassword(password: str, hashed_password):
    return bcrypt.verify(password, hashed_password)
