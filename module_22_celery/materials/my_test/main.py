from tokenize import group

from celery import chain, group, chord
from tasks import add, mul, sum_it, factorial

# Создаем группу задач
task_add = [add.s(i, i) for i in range(1 , 6)]
task_fac = [factorial.s() for i in range(2 , 7)]

group_add = group(add.s(i, i) for i in range(1 , 6))
#print(type(group_add))
group_fac = group(task_fac)

task2 = mul.s(2)
task3 = sum_it.s()
#resul = chord(task1 | sum_it.s())

res = group_add.apply_async()
#res = chain(group_add | task3).apply_async()
#print(type(res))
result = res.get()
print(result)


#my_list = [0, 2, 4, 6, 8]
#print(type(sum_it(result)))