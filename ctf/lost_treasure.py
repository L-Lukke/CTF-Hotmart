import asyncio
import websockets
import re

def max_subarray_sum(arr):
    max_atual = arr[0]
    max_global = arr[0]

    for i in range(1, len(arr)):
        max_atual = max(arr[i], max_atual + arr[i])
        if max_atual > max_global:
            max_global = max_atual

    return max_global

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

        await websocket.send("start lost_treasure")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:    
            response = await websocket.recv()
            print(f"RS: {response}")  

            linhaAnalise = await websocket.recv()
            print(f"RS: {linhaAnalise}")  
            
            linhaAnalise = extract_array_from_string(linhaAnalise)
            soma = max_subarray_sum(linhaAnalise)
            
            print(f"RU: {str(soma)}")
            await websocket.send(str(soma))

            response = await websocket.recv()
            print(f"RS: {response}")

asyncio.get_event_loop().run_until_complete(connect_to_websocket())
