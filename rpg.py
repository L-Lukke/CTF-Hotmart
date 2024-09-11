import asyncio
import websockets

def find_triplet_indices(arr, target_sum):
    n = len(arr)
    index_map = {value: idx for idx, value in enumerate(arr)}
    
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            complement = target_sum - (arr[i] + arr[j])
            if complement in index_map:
                k = index_map[complement]
                if k != i and k != j:
                    return [i, j, k]
    
    return None


async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"RS: {response}")

        await websocket.send("start rpg")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:    
            linhaAnalise = await websocket.recv()
            print(f"RS: {linhaAnalise}")  
            
            response = await websocket.recv()
            print(f"RS: {response}")  

            partes = linhaAnalise.split(' Habilidade: ')
            array_herois_str = partes[0].split('Hérois: ')[1].strip('[] ')
            habilidade = int(partes[1].strip())
            array_herois = list(map(int, array_herois_str.split(', ')))
            soma = find_triplet_indices(array_herois, habilidade)
            
            print(f"RU: {str(soma)}")
            await websocket.send(str(soma))

            response = await websocket.recv()
            print(f"RS: {response}")

asyncio.get_event_loop().run_until_complete(connect_to_websocket())
