import asyncio
import websockets
import hashlib
import base64

def decode_xor(key, text):
    textBytes = base64.b64decode(text)
    decryptedTextBytes = bytes(b ^ key for b in textBytes)
    decryptedText = decryptedTextBytes.decode('utf-8')

    return decryptedText


def decode_rot13(text):
    def rot13_char(c):
        if 'a' <= c <= 'z':
            return chr(((ord(c) - ord('a') + 13) % 26) + ord('a'))
        elif 'A' <= c <= 'Z':
            return chr(((ord(c) - ord('A') + 13) % 26) + ord('A'))
        else:
            return c

    return ''.join(rot13_char(c) for c in text)

def hash_phrase(text, method):
    if method == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif method == "sha1":
        return hashlib.sha1(text.encode()).hexdigest()
    else:
        raise ValueError("Método de hash não suportado")

def decode_phrase(text, method, key):
    if method == "hex":
        return bytes.fromhex(text).decode()
    elif method == "base64":
        return base64.b64decode(text).decode()
    elif method == "rot-13":
        return decode_rot13(text)
    elif method == "single_byte_xor":
        return decode_xor(key, text)
    elif method == "binary":
        return ''.join(chr(int(text[i:i+7], 2)) for i in range(0, len(text), 7))
    else:
        raise ValueError("Método de decodificação não suportado")

def process(text, method=None, key=None):
    if method in ["md5", "sha1"]:
        return hash_phrase(text, method)
    else:
        decoded_text = decode_phrase(text, method, key)
        return '_'.join(decoded_text.split())

async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"RS: {response}")

        await websocket.send("start cryptomix")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:
            key = None
            text = None

            response = await websocket.recv()
            print(f"RS: {response}")  

            method = await websocket.recv()
            method = method[12:-1]
            method = method.strip()
            method = str(method)
            print(f"RS: {method}")  

            text = await websocket.recv()
            text = text[13:-1]
            text = text.strip()
            text = str(text)
            print(f"RS: {text}")

            if method == "single_byte_xor":
                key = await websocket.recv()
                key = key[9:-1]
                key = key.strip()
                key = int(key, 16)
                print(f"RS: {key}")

            response = await websocket.recv()
            print(f"RS: {response}")

            response = await websocket.recv()
            print(f"RS: {response}")

            result = process(text, method=method, key=key)
            print(f"RU: {str(result)}")
            await websocket.send(str(result))

            response = await websocket.recv()
            print(f"RS: {response}")

asyncio.get_event_loop().run_until_complete(connect_to_websocket())
