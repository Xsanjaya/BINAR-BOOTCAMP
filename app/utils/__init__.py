from passlib.context import CryptContext

pwd_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")

def text2hash(text):
    return pwd_context.hash(text)
