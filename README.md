# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач" - dev-17_Python-yakovlev_vs

### Обязательная задача 1

Есть скрипт:

```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

#### Вопросы:

| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | Интерпретатор выдаст ошибку - попытка сложения целочисленного значения со строковым  |
| Как получить для переменной `c` значение 12?  | c = str(a) + b  |
| Как получить для переменной `c` значение 3?  | c = a + int(b)  |

### Обязательная задача 2

Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. 
Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

#### Мой скрипт:

Использовал свой каталог - /devops-17-netology

изменил строку поиска так как у меня стоит русифицированный git

```python
#!/usr/bin/env python3

import os

# добавляем команды для получения абсолютного пути 
bash_path = ["cd ~/devops-17-netology", "pwd"]
path = os.popen(' && '.join(bash_path)).read().rstrip() + '/'

bash_command = ["cd ~/devops-17-netology", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('изменено') != -1:
        prepare_result = result.replace('\tизменено: ', '')
        print(path + prepare_result)
        # убираем break
        # break 
```
#### Вывод скрипта при тестировании:
```bash
[root@Git-SentOS-8 ~]# python3 test.py
/root/devops-17-netology/     README.md
```
### Обязательная задача 3

- Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. 
Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

#### Мой скрипт:

```python
#!/usr/bin/env python3

import os, sys

bash_path = ""
try:
    bash_path = sys.argv[1]
except:
    print("Неверный путь к репозиторию")

if bash_path != "":
        bash_command = [f"cd {bash_path}",  "git status "]
        result_os1 = os.listdir(bash_path);

        if result_os1.__contains__(".git"):
                result_os = os.popen(' && '.join(bash_command)).read()
                for result in result_os.split('\n'):
                    if result.find('изменено') != -1:
                        prepare_result = result.replace('изменено:', bash_path)
                        print(prepare_result)
        else:
                print("По заданному пути нет репозитория git")
```

#### Вывод скрипта при тестировании:

```bash
[root@Git-SentOS-8 ~]# python3 test_git.py ~/git02_clone/
        /root/git02_clone/      README.md
        /root/git02_clone/      SECURITY.md
[root@Git-SentOS-8 ~]# python3 test_git.py ~/devops-17-netology/
        /root/devops-17-netology/      README.md
[root@Git-SentOS-8 ~]# python3 test_git.py /var/tmp
По заданному пути нет репозитория git
```
### Обязательная задача 4

Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. 
Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. 
Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. 
Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.

#### Мой скрипт:
```python
#!/usr/bin/env python3

import socket
from string import whitespace

hosts = ["drive.google.com", "mail.google.com", "google.com"]
fileList = []

with open('check_host.log') as file:
    for f in file:
        fileList.append(f)

with open('check_host.log', 'w+') as file:
    for i in hosts:
        result = socket.gethostbyname(i)
        added = 0
        for y in fileList:
            inList = y.find(" {}".format(i))
            if (inList != -1):
                ipstr=y.replace('\n', '').split("  ")[1].translate({None: whitespace})
                if (ipstr == result):
                    print(" {}  {}\n".format(i, result))
                    file.write(" {}  {}\n".format(i, result))
                    added = 1
                    break
                else:
                    print("[ERROR] {} IP mismatch: {}  {}\n".format(i, ipstr, result))
                    file.write("[ERROR] {} IP mismatch: {}  {}\n".format(i, ipstr, result))
                    added = 1
                    break
        if (added == 0):
            print(" {}  {}\n".format(i, result))
            file.write(" {}  {}\n".format(i, result))
```

#### Вывод скрипта при тестировании:

```bash
[root@Git-SentOS-8 ~]# python3 check_addr2.py
 drive.google.com  64.233.164.194

 mail.google.com  64.233.165.83

 google.com  64.233.165.139
[root@Git-SentOS-8 ~]# python3 check_addr2.py
[ERROR] drive.google.com IP mismatch: 64.233.164.194  64.233.165.194

[ERROR] mail.google.com IP mismatch: 64.233.165.83  64.233.165.17

[ERROR] google.com IP mismatch: 64.233.165.139  64.233.165.100

[root@Git-SentOS-8 ~]# python3 check_addr2.py
 drive.google.com  64.233.165.194

[ERROR] mail.google.com IP mismatch: 64.233.165.17  64.233.165.19

[ERROR] google.com IP mismatch: 64.233.165.100  64.233.165.138
```