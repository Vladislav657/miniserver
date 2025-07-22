import asyncio


HOST = "127.0.0.1"
PORT = 666


def safe_decode(data): # безопасное декодирование
    try:
        return data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return data.decode("gbk").strip()


async def check_async(reader, writer): # проверка на асинхронность
    requests = [
        b"TEST1",
        b"HELLO",
        b"GET NAME"
    ]

    for req in requests:
        writer.write(req + b"\n")
    await writer.drain()

    responses = []
    for _ in requests:
        try:
            data = await asyncio.wait_for(reader.readuntil(b"\n"), timeout=1.0)
            responses.append(safe_decode(data))
        except Exception as e:
            responses.append(f"Test error: {e}")

    if all("Test error" not in r for r in responses):
        print("Async test ok")
        for req, resp in zip(requests, responses):
            print(f"\t{safe_decode(req)}: {resp.strip()}")
        return True
    else:
        print("Async test failed")
        for req, resp in zip(requests, responses):
            print(f"\t{safe_decode(req)}: {resp}")
        return False


async def client(): # основная логика клиента
    try:
        user_data = input("Enter '<login> <password>': ").strip()
    except ValueError:
        print("Invalid input")
        return

    reader, writer = await asyncio.open_connection(HOST, PORT)
    try:
        writer.write(user_data.encode() + b"\n")
        await writer.drain()

        data = await reader.readuntil(b"\n")
        data = safe_decode(data)
        print("\nSERVER:\t" + data)
        if data != "OK":
            writer.close()
            await writer.wait_closed()
            return

        if not await check_async(reader, writer):
            writer.close()
            await writer.wait_closed()
            return

        while True:
            message = input("\nCLIENT:\t")
            writer.write(message.encode() + b"\n")
            await writer.drain()

            data = await reader.readuntil(b"\n")
            data = safe_decode(data)
            print("\nSERVER:\t" + data)

            if message.upper() == "EXIT":
                break

    except (ConnectionResetError, BrokenPipeError):
        print("SERVER DISCONNECTED")
    finally:
        writer.close()
        await writer.wait_closed()


asyncio.run(client())
