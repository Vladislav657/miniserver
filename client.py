import asyncio


HOST = "127.0.0.1"
PORT = 666


async def client():
    try:
        client_ip, client_port = input("Enter client address: ").split(':')
    except ValueError:
        print("Invalid address")
        return

    reader, writer = await asyncio.open_connection(HOST, PORT, local_addr=(client_ip, client_port))
    try:
        while True:
            message = input("CLIENT:\t").upper()
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(1024)
            print("\nSERVER:\t" + data.decode())

            if message == "EXIT":
                break

    except ConnectionResetError:
        print("SERVER DISCONNECTED")
    finally:
        writer.close()
        await writer.wait_closed()


asyncio.run(client())
