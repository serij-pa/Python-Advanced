from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    ind_start = 0
    ind_finish = len(array) - 1

    assert len(array) != 0 , "Список не должен быть пустым"

    while True:

        if number < array[ind_start]:
            ind_num = ind_start
            break

        elif number > array[ind_finish]:
            ind_num = ind_finish + 1
            break

        ind_start += 1
        ind_finish -= 1
        index_search = len(array[ind_start: ind_finish + 1]) // 2

        if array[ind_start + index_search - 1] < number < array[ind_start + index_search]:
            ind_num = ind_start + index_search
            break

        elif array[ind_start + index_search - 1] > number < array[ind_start + index_search]:
            ind_finish = ind_start + index_search

        elif array[ind_start + index_search - 1] < number > array[ind_start + index_search]:
            ind_start += index_search

    return ind_num


if __name__ == '__main__':
    #A: List[Number] = []
    #A: List[Number] = [1, 2, 3, 3, 3]
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    print(A)
    assert A == sorted(A)
