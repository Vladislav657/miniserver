# Запуск сервера и клиентов

```bash
# Запуск сервера (в первом терминале)
python server.py
```
```bash
# Запуск клиентов (во втором терминале)
Enter '<login> <password>': <login> <password> # необходимо ввести логин пароль

SERVER: OK # если логин существует, то проверяется пароль, если верный - "OK", иначе - "WRONG PASSWORD"
           # если логин не существует, то введённые логин и пароль добавляются и выводится "OK"

# далее идёт тест на асинхронную реакцию, если пройден - "Async test ok", иначе - "Async test failed"
Async test ok
TEST1: ERROR
HELLO: HI!
GET NAME: NAME NOT FOUND
```
```bash
python client.py # (в третьем терминале)
Enter '<login> <password>': <login> <password>

...
# и т. д. каждый клиент в своем терминале
```
В окне сервера при установке соединения выводится сообщение:
```bash
Connection from <ip>:<port>
```
# Тестирование сервера
Для тестирования в окнах клиентов вводите следующие команды (допускается нижний регистр):
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
Если команда неизвестна — ERROR.

# Пример работы сервера
```bash
# клиент

python client.py
Enter '<login> <password>': wassup 42

SERVER: OK
Async test ok
        TEST1: ERROR
        HELLO: HI!
        GET NAME: NAME NOT FOUND

CLIENT: set name meow

SERVER: OK


SERVER: HI!

CLIENT: get name

SERVER: NAME meow

CLIENT: exit

SERVER: MISSION ACCOMPLISHED

python client.py
Enter '<login> <password>': wassup 42

SERVER: OK
Async test ok
        TEST1: ERROR
        HELLO: HI!
        GET NAME: NAME meow

CLIENT: get name

SERVER: NAME meow

CLIENT: exit

SERVER: MISSION ACCOMPLISHED
```
```bash
# сервер

python server.py
Connection from 127.0.0.1:51714
Connection from 127.0.0.1:51714 closed
Connection from 127.0.0.1:51736
Connection from 127.0.0.1:51736 closed
```
