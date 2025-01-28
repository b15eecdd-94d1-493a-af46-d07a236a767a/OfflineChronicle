import subprocess
import argparse
import sys
import os
import re
# Путь к каталогу, в котором нужно искать файлы
directory = 'template'

# Регулярное выражение для поиска файлов с названием blog_template_{num}.html
pattern = re.compile(r'blog_template_([a-zA-Z0-9]+)\.html')

# Список для хранения найденных чисел {num}
designs = []
# Проходим по всем файлам в каталоге
for filename in os.listdir(directory):
    # Проверяем, соответствует ли имя файла шаблону
    match = pattern.match(filename)
    if match:
        # Если соответствует, извлекаем число и добавляем его в список
        designs.append(match.group(1))
designs = sorted(designs)
default_design = designs[0]
# Количество найденных файлов


parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-n", "--blogname", help="Название блога", type=str, default="blog")
parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
parser.add_argument("-l", "--limit", help="Максимальное количество постов на одной странице", type=int, default=50)
parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="DESC")
parser.add_argument("-d", "--design", help="Дизайн", type=str, choices=designs, default=default_design)
parser.add_argument("-p", "--port", help="Порт", type=int, default=5050)
parser.add_argument("-ro", "--readonly", help="Режим без возможности управлять записями", type=str, choices=["Y", "N"], default="N")
parser.add_argument("-h2", "--host", help="Хост", type=str, default="127.0.0.1")
parser.add_argument("-lh", "--localhost", help="Запретить доступ из внешней сети", type=str, choices=["Y", "N"], default="Y")
parser.add_argument("-ai", "--admin-ip", help="IP-адрес администратора (допустимо перечислять через пробел)", type=str, default="127.0.0.1")
parser.add_argument("-l2", "--log", help="Выводить лог в консоль", type=str, choices=["Y", "N"], default="Y")

args = parser.parse_args()
args = vars(args)
new_env = {**os.environ}
for arg_name in args:
    new_env[arg_name] = str(args[arg_name])
flask = subprocess.run(['flask', '--app', 'lib/flask_server', 'run', '--host', str(args['host']), '--port', str(args['port'])], env=new_env)