# Предупреждение
local_blog создан для работы на 127.0.0.1, автор отказывается от любой ответственности за понесённый ущерб в случае открытия доступа к блогу через Интернет.

# Порядок установки
Создайте локальное окружение: python3 -m example_blog_venv

Перейдите в локальное окружение: source example_blog_venv/bin/activate

Скачайте зависимости: pip install -r requirements.txt

### Список записей
```
usage: python3 list.py [-h] [-n NAME] [-l LIMIT] [-p PAGE] [-s {DESC,ASC}]
                       [-sep SEPARATOR] [-w WIDTH] [-tz TIMEZONE]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
  -l LIMIT, --limit LIMIT
                        Максимальное количество записей (default: 50)
  -p PAGE, --page PAGE  Номер страницы (default: -1)
  -s {DESC,ASC}, --sort {DESC,ASC}
                        Сортировка (default: ASC)
  -sep SEPARATOR, --separator SEPARATOR
                        Разделитель между постами (default:
                        ----------------------------------------)
  -w WIDTH, --width WIDTH
                        Максимальная ширина строки (default: 40)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default:
                        local)

```

### Добавить запись в блог.
```
usage: python3 add.py [-h] [-n NAME]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
```

### Удалить запись по id.
```
usage: python3 delete.py [-h] [-n NAME] [-sd {Y,N}]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
  -sd {Y,N}, --soft-deletion {Y,N}
                        Мягкое удаление (default: N)
```

### Получить запись по id.
```
usage: python3 get_by_id.py [-h] [-n NAME] [-sep SEPARATOR] [-w WIDTH]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
  -sep SEPARATOR, --separator SEPARATOR
                        Разделитель между постами (default:
                        ----------------------------------------)
  -w WIDTH, --width WIDTH
                        Максимальная ширина строки (default: 40)
```
### Поиск
```
usage: python3 search.py [-h] [-n NAME] [-s {DESC,ASC}] [-sep SEPARATOR]
                         [-w WIDTH] [-tz TIMEZONE]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
  -s {DESC,ASC}, --sort {DESC,ASC}
                        Сортировка (default: DESC)
  -sep SEPARATOR, --separator SEPARATOR
                        Разделитель между постами (default:
                        ----------------------------------------)
  -w WIDTH, --width WIDTH
                        Максимальная ширина строки (default: 40)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default:
                        local)
```

### Лог
```
usage: python3 get_all_log_records.py [-h] [-n NAME] [-tz TIMEZONE]
                                      [-sep SEPARATOR] [-s {DESC,ASC}]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default:
                        local)
  -sep SEPARATOR, --separator SEPARATOR
                        Разделитель между постами (default:
                        ----------------------------------------)
  -s {DESC,ASC}, --sort {DESC,ASC}
                        Сортировка (default: ASC)
```
### Поднять локальный сервер.
```
usage: python3 server.py [-h] [-n BLOGNAME] [-tz TIMEZONE] [-l LIMIT]
                         [-s {DESC,ASC}] [-d {1,2,3,4,5,custom}] [-p PORT]
                         [-ro {Y,N}] [-h2 HOST] [-lh {Y,N}] [-ai ADMIN_IP]
                         [-l2 {Y,N}]

options:
  -h, --help            show this help message and exit
  -n BLOGNAME, --blogname BLOGNAME
                        Название блога (default: blog)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default:
                        local)
  -l LIMIT, --limit LIMIT
                        Максимальное количество постов на одной странице
                        (default: 50)
  -s {DESC,ASC}, --sort {DESC,ASC}
                        Сортировка (default: DESC)
  -d {1,2,3,4,5,custom}, --design {1,2,3,4,5,custom}
                        Дизайн (default: 1)
  -p PORT, --port PORT  Порт (default: 5050)
  -ro {Y,N}, --readonly {Y,N}
                        Режим без возможности управлять записями (default: N)
  -h2 HOST, --host HOST
                        Хост (default: 127.0.0.1)
  -lh {Y,N}, --localhost {Y,N}
                        Запретить доступ из внешней сети (default: Y)
  -ai ADMIN_IP, --admin-ip ADMIN_IP
                        IP-адрес администратора (допустимо перечислять через
                        пробел) (default: 127.0.0.1)
  -l2 {Y,N}, --log {Y,N}
                        Выводить лог в консоль (default: Y)
```
### GUI
```
usage: python3 gui.py [-h] [-n BLOGNAME] [-tz TIMEZONE] [-l LIMIT]
                      [-s {DESC,ASC}]

options:
  -h, --help            show this help message and exit
  -n BLOGNAME, --blogname BLOGNAME
                        Название блога (default: blog)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default:
                        local)
  -l LIMIT, --limit LIMIT
                        Максимальное количество постов на одной странице
                        (default: 50)
  -s {DESC,ASC}, --sort {DESC,ASC}
                        Сортировка (default: DESC)
```
