#!/usr/bin/env python3

import os

bash_command = ["cd  C:/Users/Valdem88/PycharmProjects/dev-17_Python-yakovlev_vs", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('изменено') != -1:
        prepare_result = result.replace('\tизменено:   ', '')
        print(prepare_result)
        break
