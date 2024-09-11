import asyncio
import websockets

def is_happy_number(n):
    def sum_of_squares(num):
        return sum(int(digit) ** 2 for digit in str(num))

    visited = set()
    
    while n != 1 and n not in visited:
        visited.add(n)
        n = sum_of_squares(n)
    
    return n == 1

async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"Response from server: {response}")

        await websocket.send("start behappy")

        response = await websocket.recv()
        print(f"Response from server: {response}")

        while True:
            response = await websocket.recv()
            print(f"Response from server: {response}")
            
            num = await websocket.recv()
            num = num[12:]
            print(f"Response from server: {num}")

            if is_happy_number(int(num)):
                await websocket.send("Feliz")
                print(f"Feliz")
            else:
                await websocket.send("Infeliz")
                print(f"Infeliz")

            response = await websocket.recv()
            print(f"Response from server: {response}")


            

            


# Run the client
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
