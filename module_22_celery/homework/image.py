# https://pythonru.com/biblioteki/osnovnye-vozmozhnosti-biblioteki-python-imaging-library-pillow-pil
"""
Здесь происходит логика обработки изображения
"""

from typing import Optional

from PIL import Image, ImageFilter


def blur_image(src_filename):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    #if not dst_filename:
    #    dst_filename = f'blur_{src_filename}'

    with Image.open(src_filename) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        list_path_file = src_filename.split("/")
        new_name_img = (f"{list_path_file[0]}/{list_path_file[1]}/{list_path_file[2]}/blur_{list_path_file[3]}")

        new_img.save(new_name_img)
        return new_name_img
