# Запуск сервера и клиентов

```bash
# Запуск сервера (в первом терминале)
python server.py
```
```bash
# Запуск клиентов (во втором терминале)
python client.py
Enter client address: 127.6.7.9:50000 # указать ip:port клиента
```
```bash
python client.py # (в третьем терминале)
Enter client address: <ip>:<port>

# и т. д. каждый клиент в своем терминале
```
В окне сервера при установке соединения выводится сообщение:
```bash
Connection from <ip>:<port>
```
# Тестирование сервера
Для тестирования в окнах клиентов вводите следующие команды:
1.	SET NAME <device_name>
2.	GET NAME
3.	HELLO
4.	EXIT

Сервер должен отвечать:
1.	OK — при SET NAME <device_name>;
2.	NAME <device_name> — при GET NAME;
3.	HI! — при HELLO;
4.	MISSION ACCOMPLISHED — при EXIT, и закрывает соединение, при этом в окне сервера будет выведено:
```bash
Connection from <ip>:<port> closed
```

# Пример работы сервера
```bash
# первый клиент

python client.py
Enter client address: 127.6.7.9:50000
CLIENT: set name 54
SERVER: OK

CLIENT: get name

SERVER: NAME 54

CLIENT: exit

SERVER: MISSION ACCOMPLISHED

python client.py
Enter client address: 127.6.7.9:50000
CLIENT: get name

SERVER: NAME 54

CLIENT: exit

SERVER: MISSION ACCOMPLISHED
```
```bash
# второй клиент

python client.py
Enter client address: 127.5.3.2:55499
CLIENT: set name 65

SERVER: OK

CLIENT: get name 

SERVER: NAME 65

CLIENT: exit

SERVER: MISSION ACCOMPLISHED
```
```bash
# сервер

python server.py
Connection from 127.5.3.2:55499
Connection from 127.6.7.9:50000
Connection from 127.6.7.9:50000 closed
Connection from 127.6.7.9:50000
Connection from 127.5.3.2:55499 closed
Connection from 127.6.7.9:50000 closed
```
