import asyncio
import re


HOST = "127.0.0.1"
PORT = 666
names = {}
passwords = {}

names_lock = asyncio.Lock()
passwords_lock = asyncio.Lock()


def safe_decode(data): # безопасное декодирование
    try:
        return data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return data.decode("gbk").strip()


async def handle_client(reader, writer): # основная логика сервера
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr[0]}:{addr[1]}")

    try:
        data = await reader.readuntil(b"\n")
        data = safe_decode(data)
        login, password = data.split()
        async with passwords_lock:
            if login not in passwords:
                passwords[login] = password
                writer.write(b"OK\n")
            elif password != passwords[login]:
                writer.write(b"WRONG PASSWORD\n")
            else:
                writer.write(b"OK\n")
        await writer.drain()

    except ValueError:
        writer.write(b"Invalid input\n")
        await writer.drain()
        writer.close()
        print(f"Connection from {addr[0]}:{addr[1]} closed")
        await writer.wait_closed()
        return

    try:
        while True:
            data = await reader.readuntil(b"\n")
            data = safe_decode(data)
            if data == '':
                break
            if data.upper().startswith('SET NAME '):
                name = data.split()[2]
                if re.match(r"^[a-zA-Z0-9@-]+$", name):
                    async with names_lock:
                        names[login] = name
                    writer.write(b"OK\n")
                else:
                    writer.write(b"INVALID NAME\n")
            else:
                data = data.upper()
                if data == 'GET NAME':
                    async with names_lock:
                        ans = f"NAME {names[login]}\n" if login in names else "NAME NOT FOUND\n"
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


async def main(): # запуск сервера
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()


asyncio.run(main())
