import asyncio


HOST = "127.0.0.1"
PORT = 666
names = {}


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr[0]}:{addr[1]}")
    try:
        while True:
            data = (await reader.read(1024)).decode().strip()
            if data.startswith('SET NAME '):
                names[addr] = data.split()[-1]
                writer.write(b"OK\n")
            elif data == 'GET NAME':
                ans = f"NAME {names[addr]}\n" if addr in names else "NAME NOT FOUND\n"
                writer.write(ans.encode())
            elif data == 'HELLO':
                writer.write(b"HI!\n")
            elif data == 'EXIT':
                writer.write(b"MISSION ACCOMPLISHED\n")
                break
            else:
                writer.write(b"ERROR\n")

            await writer.drain()
    finally:
        writer.close()
        print(f"Connection from {addr[0]}:{addr[1]} closed")
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()


asyncio.run(main())
