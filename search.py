import asyncio
import websockets
import re

def extract_array_from_string(s):
    match = re.search(r'\[([-\d, ]+)\]', s)
    if match:
        array_str = match.group(1)
        array = [int(num) for num in array_str.split(', ')]
        return array
    else:
        return None
    
    
async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"RS: {response}")

        await websocket.send("start search")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:            
            array = await websocket.recv()
            print(f"RS: {array}")

            target = await websocket.recv()
            print(f"RS: {target}")

            response = await websocket.recv()
            print(f"RS: {response}")

            array = extract_array_from_string(array)
            target = target[12:]
            target.strip()
            target = int(target)

            index = array.index(target)

            await websocket.send(str(index))
            print(f"RU: {str(index)}")

            response = await websocket.recv()
            print(f"RS: {response}")
            
            

# Run the client
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
