import io
import base64
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

def encode_image(img):
    try:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_data = buffer.getvalue()
        encoded_image = base64.b64encode(img_data)
        return encoded_image.decode('utf-8')
    except Exception as e:
        print("Error:", e)

def decode_image(encoded_image):
    try:
        decoded_data = base64.b64decode(encoded_image.encode('utf-8'))
        img = Image.open(io.BytesIO(decoded_data))
        return img
    except Exception as e:
        print("Error:", e)

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