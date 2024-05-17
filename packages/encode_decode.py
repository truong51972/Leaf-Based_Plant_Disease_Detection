import base64
import pickle

from PIL import Image

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt_password(password: str) -> bytes:
    password = password.encode('UTF-8')  
    salt = password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    encrypted_password = base64.urlsafe_b64encode(kdf.derive(password))
    return encrypted_password

def encode_image(image: Image.Image) -> str:
    encoded_image = pickle.dumps(image).decode('latin-1')
    return encoded_image

def decode_image(encoded_image: str) -> Image.Image:
    image = pickle.loads(encoded_image.encode('latin-1'))
    return image

if __name__ == '__main__':

    # encrypted_password = encrypt_password('chao em')
    # print(encrypted_password)
    # # Sử dụng key với Fernet
    # # f = Fernet(key)
    image = Image.open('fb logo.png')
    print(image)

    encoded_image = encode_image(image)
    print(encoded_image==encoded_image)
    print(type(encoded_image))

    decoded_image = decode_image(encoded_image)
    print(decoded_image)