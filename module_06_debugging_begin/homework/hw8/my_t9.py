"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
import re
from typing import List

symbol_num = {1: "\\.\\!\\?", 2: "abc", 3: "def", 4: "ghi", 5: "jkl", 6: "mno", 7: "pqrs", 8: "tuv", 9: "wxyz"}

def my_t9(input_numbers: str) -> List[str]:
    with open("words.txt", "r") as file:
        list_words = list(filter(lambda x: x, file))
    symbol = (map(lambda y: "[" + symbol_num[int(y)] + "]", input_numbers))
    list_symbol = "^" + "".join(symbol) + "$"
    similar_words = [lw.rstrip() for lw in list_words if re.search(list_symbol, lw, re.IGNORECASE)]
    return similar_words


if __name__ == '__main__':
    #numbers: str = input()
    numbers: str = "22736368"
    #my_t9(numbers)
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')
