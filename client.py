import asyncio


HOST = "127.0.0.1"
PORT = 666


def safe_decode(data):
    try:
        return data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return data.decode("gbk").strip()


async def client():
    try:
        user_data = input("Enter '<login> <password>': ").strip()
    except ValueError:
        print("Invalid input")
        return

    reader, writer = await asyncio.open_connection(HOST, PORT)
    try:
        writer.write(user_data.encode())
        await writer.drain()

        data = await reader.read(1024)
        data = safe_decode(data)
        print("\nSERVER:\t" + data)
        if data != "OK":
            writer.close()
            await writer.wait_closed()
            return

        while True:
            message = input("\nCLIENT:\t")
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(1024)
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
