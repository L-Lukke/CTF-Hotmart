import ast
import asyncio
import websockets
import heapq

def dijkstra(graph, start):
    # Inicializa as distâncias de todos os vértices para infinito, exceto o ponto inicial
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    # Fila de prioridade para os vértices a serem explorados
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Se a distância atual for maior que a distância registrada, ignore
        if current_distance > distances[current_vertex]:
            continue
        
        # Explora os vizinhos do vértice atual
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            
            # Se encontrar um caminho mais curto, atualize a distância e adicione à fila
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def create_graph(edges):
    graph = {}
    for start, end, weight in edges:
        if start not in graph:
            graph[start] = {}
        if end not in graph:
            graph[end] = {}
        graph[start][end] = weight
        graph[end][start] = weight
    return graph

async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"RS: {response}")

        await websocket.send("start uailog")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:
            ruas = await websocket.recv()
            ruas = ruas[10:]
            print(f"RS: {ruas}")
            ruas = ast.literal_eval(ruas)
            grafo = create_graph(ruas)

            origem = await websocket.recv()
            origem = origem[-2:]
            origem.strip()
            origem = list(origem)
            origem = origem[0]
            print(f"RS: {origem}")

            distancias = dijkstra(grafo, origem)

            destino = await websocket.recv()
            destino = destino[-2:]
            destino.strip()
            destino = list(destino)
            destino = destino[0]
            print(f"RS: {destino}")

            distancia_minima = distancias[destino]
            distancia_minima = str(distancia_minima)

            await websocket.send(distancia_minima)
            print(f"RU: {distancia_minima}")

            response = await websocket.recv()
            print(f"RS: {response}")
            
            response = await websocket.recv()
            print(f"RS: {response}")
            
# Run the client
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
