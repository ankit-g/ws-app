import asyncio
import websockets


async def sender(ws, q):
    while True:
        await ws.send(await q.get())

async def recever(ws, q):
    while True:
        msg = await ws.recv()
        print(f"r> {msg}")


async def shell(queue):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
                    sender(websocket, queue),
                    recever(websocket, queue))

async def get_input(queue):
    banner = None
    while True:
        banner = "Your ID: " if not banner else ">> "
        msg = await asyncio.to_thread(input, banner)  # Run input in a separate thread
        await queue.put(msg)

async def main():
    queue = asyncio.Queue()
    tasks = [
        shell(queue),
        get_input(queue)
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
