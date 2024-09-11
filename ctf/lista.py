import asyncio
import websockets
import re

def extract_array_from_string(s):
    # Use regular expression to find the array within the string
    match = re.search(r'\[([-\d, ]+)\]', s)
    if match:
        # Extract the array as a string and split it into individual elements
        array_str = match.group(1)
        # Convert the split string elements to integers
        array = [int(num) for num in array_str.split(', ')]
        return array
    else:
        return None
    
def reorganize_list(nums):
    pares = [num for num in nums if num % 2 == 0]
    impares = [num for num in nums if num % 2 != 0]
    return pares + impares

def list_to_string(nums):
    return str(nums)
    
async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"RS: {response}")

        await websocket.send("start organizer")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:            
            word = await websocket.recv()
            print(f"RS: {word}")

            response = await websocket.recv()
            print(f"RS: {response}")

            words = extract_array_from_string(word)
            resp = reorganize_list(words)
            resp_string = list_to_string(resp)
            await websocket.send(resp_string)
            print(f"RU: {resp_string}")

            response = await websocket.recv()
            print(f"RS: {response}")
            
            

# Run the client
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
