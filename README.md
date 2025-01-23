Установка зависимостей: pip install -r requirements.txt

###python3 list.py - список записей
```
usage: python list.py [-h] [-n NAME] [-l LIMIT] [-p PAGE] [-s {DESC,ASC}] [-sep SEPARATOR] [-w WIDTH] [-tz TIMEZONE]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
  -l LIMIT, --limit LIMIT
                        Максимальное количество записей (default: 50)
  -p PAGE, --page PAGE  Номер страницы (default: 1)
  -s {DESC,ASC}, --sort {DESC,ASC}
                        Сортировка (default: DESC)
  -sep SEPARATOR, --separator SEPARATOR
                        Разделитель между постами (default: ----------------------------------------)
  -w WIDTH, --width WIDTH
                        Максимальная ширина строки (default: 40)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default: local)

```

###python3 add.py - добавить запись в блог.
```
usage: python add.py [-h] [-n NAME]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
```

###python3 delete.py - удалить запись по id.
```
usage: python delete.py [-h] [-n NAME]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
```

###python3 get_by_id.py - получить запись по id.
```
usage: python get_by_id.py [-h] [-n NAME] [-sep SEPARATOR] [-w WIDTH]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Название блога (default: blog)
  -sep SEPARATOR, --separator SEPARATOR
                        Разделитель между постами (default: ----------------------------------------)
  -w WIDTH, --width WIDTH
                        Максимальная ширина строки (default: 40)
```
