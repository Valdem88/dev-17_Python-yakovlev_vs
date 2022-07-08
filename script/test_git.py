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