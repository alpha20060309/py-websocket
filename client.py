import asyncio
import websockets

async def connect():
    uri = "ws://localhost:4000"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from Dilbek!")
        response = await websocket.recv()
        print(f"Received from server: {response}")

asyncio.get_event_loop().run_until_complete(connect())
