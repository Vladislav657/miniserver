import asyncio
import random


HOST = "127.0.0.1"
PORT = 666


def safe_decode(data): # безопасное декодирование
    try:
        return data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return data.decode("gbk").strip()


async def auth(reader, writer, client_id): # логин/пароль для теста
    auth_data = f"user{client_id} pass{client_id}"
    writer.write(f"{auth_data}\n".encode())
    await writer.drain()

    response = await reader.readuntil(b"\n")
    return safe_decode(response).strip() == "OK"


async def async_test_client(client_id): # запуск тестирующего клиента
    reader, writer = await asyncio.open_connection(HOST, PORT)
    try:
        if not await auth(reader, writer, client_id):
            print(f"Client {client_id}: auth error")
            return False

        commands = [
            f"SET NAME Client{client_id}",
            "GET NAME",
            "HELLO"
        ]
        cmd = random.choice(commands)

        writer.write(f"{cmd}\n".encode())
        await writer.drain()

        response = await reader.readuntil(b"\n")
        print(f"Client {client_id}: {cmd} -> {safe_decode(response).strip()}")

    except Exception as e:
        print(f"Client {client_id} error: {str(e)}")
        return False

    finally:
        writer.close()
        await writer.wait_closed()
        return True


async def test_async(num_clients): # подключение num_clients клиентов
    tasks = [async_test_client(i) for i in range(1, num_clients + 1)]
    results = await asyncio.gather(*tasks)

    successful = sum(results)
    print(f"\nResult: {successful} of {len(results)} clients ok")
    return successful == num_clients


async def client(): # основная логика клиента
    num_clients = int(input("Enter number of clients for async test: "))
    if not await test_async(num_clients):
        print("Async test failed")
        return

    print(f"Async test ok")
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
