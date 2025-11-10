from cats_coroutine import main_corot
from cats_threading import main_thread
from cats_multiprocessing import main_multiproc
from contextlib import redirect_stdout
from py_markdown_table.markdown_table import markdown_table

uploading_images = [10, 50, 100]

def get_time(up_images):
    report = []
    for i_image in up_images:
        time_thread = main_thread(i_image)
        time_multiproc = main_multiproc(i_image)
        time_corot = main_corot(i_image)
        report.append(
            {
                'cats_we_want': i_image,
                'time_thread': time_thread,
                'time_multiproc': time_multiproc,
                'time_coro': time_corot,
            }
        )

    print('Сформирован файл REPORT.MD')
    markdown = markdown_table(report).get_markdown()
    with open('REPORT.MD', 'w') as f:
        with redirect_stdout(f):
            print('Отчет о выполнении программы:\n')
            print(markdown)


if __name__ == '__main__':
    get_time(uploading_images)