import asyncio
import websockets
import json

# Update with local values
SUPABASE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE = "test"
SCHEMA = "public"

SUPABASE_REALTIME_URL = "ws://localhost:8000/realtime/v1/websocket"

async def connect():
    async with websockets.connect(f"{SUPABASE_REALTIME_URL}?apikey={SUPABASE_JWT}") as websocket:
        print("[✅] Connected to local Supabase Realtime")

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
                else:
                    print(f"[📨] Event: {message.get('event')} - Topic: {message.get('topic')}")
            except Exception as e:
                print(f"[❌] Error: {e}")
                break

asyncio.run(connect())
