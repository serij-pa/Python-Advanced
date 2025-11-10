"""
Напишите код, который выводит сам себя.
Обратите внимание, что скрипт может быть расположен в любом месте.
"""

file = open("self_printing.py", "r")
print(file.read().rstrip())
file.close()

result = 0
for n in range(1, 11):
    result += n ** 2

# Secret magic code