import asyncio
import websockets

def is_palindrome(s):
    return s == s[::-1]

def longest_palindrome_substring(s):
    n = len(s)

    if n == 0:
        return ""
    
    longest = ""
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if is_palindrome(substring) and len(substring) > len(longest):
                longest = substring

    if len(longest) == 1:
        return "Sem palindromo"
    if len(longest) == 0:
        return "Sem palindromo"
    
    return longest

async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"Response from server: {response}")

        await websocket.send("start palindromo")

        response = await websocket.recv()
        print(f"Response from server: {response}")

        while True:
            response = await websocket.recv()
            print(f"Response from server: {response}")
            
            word = await websocket.recv()
            print(f"Response from server: {word}")
            words = word.split()
            print(longest_palindrome_substring(words[-1]))
            await websocket.send(longest_palindrome_substring(words[-1]))

            response = await websocket.recv()
            print(f"Response from server: {response}")


            

            


# Run the client
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
