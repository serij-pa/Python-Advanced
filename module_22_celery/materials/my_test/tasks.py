from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    res_mul = x * y
    return f"{res_mul}"

@app.task
def sum_it(numbers):
    return sum(numbers)

@app.task
def factorial():
    result = 1
    for i in range(1, 10):
        result *= i
    return f"{result}"