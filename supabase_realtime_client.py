import asyncio
import websockets
import json

SUPABASE_PROJECT_ID = "duiziaafqnukalllcpoh"  # e.g., xyzcompanyabc
SUPABASE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1aXppYWFmcW51a2FsbGxjcG9oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMyNDgwNjIsImV4cCI6MjA2ODgyNDA2Mn0.hX7xtMXsszQQHhl-eNoNeHcY0A1-ue-qjyamJgES9Cc"
TABLE = "test"  # The table you want to listen to
SCHEMA = "public"

SUPABASE_REALTIME_URL = f"wss://{SUPABASE_PROJECT_ID}.supabase.co/realtime/v1/websocket"

async def connect():
    async with websockets.connect(f"{SUPABASE_REALTIME_URL}?apikey={SUPABASE_JWT}") as websocket:
        print("[✅] Connected to Supabase Realtime")

        # Join channel
        join_msg = {
            "topic": f"realtime:{SCHEMA}.{TABLE}",
            "event": "phx_join",
            "payload": {
                "config": {
                    "broadcast": {"self": False},
                    "postgres_changes": [
                        {
                            "event": "*",
                            "schema": SCHEMA,
                            "table": TABLE
                        }
                    ]
                },
                "user_token": SUPABASE_JWT
            },
            "ref": "1"
        }

        await websocket.send(json.dumps(join_msg))
        print(f"[📡] Subscribed to realtime:{SCHEMA}.{TABLE}")

        # Receive loop
        while True:
            try:
                raw = await websocket.recv()
                message = json.loads(raw)
                if message.get("event") == "postgres_changes":
                    record = (
                        message.get("payload", {})
                        .get("data", {})
                        .get("record")
                    )
                    print(f"[🔄] Record: {json.dumps(record, indent=2)}")
            except Exception as e:
                print(f"[❌] Error: {e}")
                break

asyncio.run(connect())
