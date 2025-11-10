"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    result_line = ""
    with open(ps_output_file_path, "r", encoding="utf-8") as output_file:
        lines = output_file.readlines()[1:]
        for i_line in lines:
            columns = int(i_line.split()[5])
            if columns > 0:
                if columns > 1024:
                    result_line += f"{round(int(columns) / 1024)} Кб\n"
                elif columns > 1048576:
                    result_line += f"{round(int(columns) / 1048576)} Мб\n"
                else:
                    result_line += f"{columns} Б\n"
            else:
                continue
        return result_line




if __name__ == '__main__':
    # path: str = 'PATH_TO_OUTPUT_FILE'
    path: str = "output_file.txt"
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
