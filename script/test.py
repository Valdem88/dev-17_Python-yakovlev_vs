#!/usr/bin/env python3

import os

# добавляем команды для получения абсолютного пути
bash_command_path = ["cd ~/netology/sysadm-homeworks", "pwd"]
path = os.popen(' && '.join(bash_command_path)).read().rstrip() + '/'

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified: ', '')
        print(path + prepare_result)
        # убираем break
        # break