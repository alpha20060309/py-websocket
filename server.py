import asyncio
import websockets

# NEW signature: only 1 argument
async def echo(websocket):
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: Hello from Komol")
    except Exception as e:
        print(f"Server error: {e}")

async def main():
    async with websockets.serve(echo, "localhost", 4000):
        print("WebSocket server running at ws://localhost:4000")
        await asyncio.Future()  # Run forever

asyncio.run(main())
