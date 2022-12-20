from passlib.context import CryptContext

# We are using bcypt algo to hash the password
#For the security purpose we need to use hashing so in order to achieve this install passlib[bcrypt] and add import them from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)


def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)