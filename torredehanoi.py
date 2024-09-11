import asyncio
import websockets
import re

def parse_mission_details(missao):
    x_match = re.search(r'Príncipes:\s*\[(\d+)\]', missao)
    y_match = re.search(r'Movimentos Mínimos Necessários:\s*\[(\d+)\]', missao)
    
    x = int(x_match.group(1)) if x_match else None
    y = int(y_match.group(1)) if y_match else None
    
    return x, y

def hanoi(n, origem, destino, auxiliar):
    if n == 1:
        return [(origem, destino)]
    else:
        movimentos = hanoi(n - 1, origem, auxiliar, destino)
        movimentos.append((origem, destino))
        movimentos += hanoi(n - 1, auxiliar, destino, origem)
        return movimentos

def resolver_torre_hanoi(principes):
    origem = 'A'
    destino = 'C'
    auxiliar = 'B'
    return hanoi(principes, origem, destino, auxiliar)
    
    
async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"RS: {response}")

        await websocket.send("start towerofhanoi")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:            
            missao = await websocket.recv()
            print(f"RS: {missao}")

            principes, movimentos = parse_mission_details(missao)

            movimentos_minimos = resolver_torre_hanoi(principes)       

            await websocket.send(str(movimentos_minimos))
            print(f"RU: {str(movimentos_minimos)}")

            response = await websocket.recv()
            print(f"RS: {response}")
            
asyncio.get_event_loop().run_until_complete(connect_to_websocket())