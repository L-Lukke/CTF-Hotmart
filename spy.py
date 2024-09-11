import asyncio
import websockets

def preprocess_map(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Clone the matrix to work on it
    processed_matrix = [list(row) for row in matrix]
    
    # Process vertical obstacles (up and down)
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == '^':
                for i in range(r - 1, -1, -1):
                    if matrix[i][c] == '🏠' or i < 0:
                        break
                    if i > 0 and (matrix[i-1][c] in ['>', '<', 'v']):
                        break
                    processed_matrix[i][c] = 'N'
            elif matrix[r][c] == 'v':
                for i in range(r + 1, rows):
                    if i >= rows or matrix[i][c] == '🏠':
                        break
                    if i < rows - 1 and (matrix[i+1][c] in ['>', '<', '^']):
                        break
                    processed_matrix[i][c] = 'N'

    # Process lateral obstacles (left and right)
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == '<':
                for i in range(c - 1, -1, -1):
                    if matrix[r][i] == '🏠' or i < 0:
                        break
                    if i > 0 and (matrix[r][i-1] in ['>', 'v', '^']):
                        break
                    processed_matrix[r][i] = 'N'
            elif matrix[r][c] == '>':
                for i in range(c + 1, cols):
                    if i >= cols or matrix[r][i] == '🏠':
                        break
                    if i < cols - 1 and (matrix[r][i+1] in ['<', 'v', '^']):
                        break
                    processed_matrix[r][i] = 'N'

    
    return processed_matrix

def is_path_available(matrix, start, end):
    from collections import deque
    
    rows = len(matrix)
    cols = len(matrix[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = [[False] * cols for _ in range(rows)]
    
    queue = deque([start])
    visited[start[0]][start[1]] = True
    
    while queue:
        r, c = queue.popleft()
        
        if (r, c) == end:
            return True
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                if matrix[nr][nc] in ('_', '💻'):
                    visited[nr][nc] = True
                    queue.append((nr, nc))
    
    return False

def existeounao(matrix):
    processed_matrix = preprocess_map(matrix)
    
    start = None
    end = None
    
    for r in range(len(processed_matrix)):
        for c in range(len(processed_matrix[0])):
            if processed_matrix[r][c] == '🥷':
                start = (r, c)
            elif processed_matrix[r][c] == '💻':
                end = (r, c)
    
    if start and end:
        if is_path_available(processed_matrix, start, end):
            return "Vai!"
        else:
            return "Espere!"
    else:
        return "Espere!"

async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"

    async with websockets.connect(uri) as websocket:

        response = await websocket.recv()
        print(f"RS: {response}")

        await websocket.send("start spy")

        response = await websocket.recv()
        print(f"RS: {response}")

        while True:            
            mapa = await websocket.recv()
            print(f"RS: {mapa}")       

            lines = mapa.split('\n')
            lines.pop(0)
            lines.pop()
            parsed_list = [list(line) for line in lines]

            await websocket.send(existeounao(parsed_list))
            print(existeounao(parsed_list))


            response = await websocket.recv()
            print(f"RS: {response}")
            
            

# Run the client
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
