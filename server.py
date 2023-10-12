import asyncio
import websockets
import time

clients={}

async def ws_handler(ws):
        _uid = await ws.recv()
        clients[_uid]=ws
        print(_uid)
        async for msg in ws:
            print(msg)
            try:
                cmd, _rid, *msg = msg.split()
            except ValueError:
                print("Bkws CMD")
                continue
            if 's' != cmd:
                await ws.send(f"Incorrect CMD")
                continue
            if _rid not in clients:
                await ws.send(f"Incorrect RID")
                continue
            await clients[_rid].send(' '.join(msg))



async def ws_server():
    async with websockets.serve(ws_handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(ws_server())


