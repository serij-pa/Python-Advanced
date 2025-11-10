import subprocess


def process_count(username: str) -> int:
    list_flags = ["ps", "-u", username, "-o", "pid"]
    proc = subprocess.run(list_flags, capture_output=True)
    list_proc = len(proc.stdout.decode().splitlines()[1:])
    print(f"Количество процессов, запущенных из-под {username} {list_proc} шт.")
    # количество процессов, запущенных из-под
    # текущего пользователя username
    #pass


def total_memory_usage(root_pid: int) -> float:
    list_flags = ["ps", "--ppid", str(root_pid), "-o", "%mem="]
    proc = subprocess.run(list_flags, capture_output=True)
    list_proc = proc.stdout.decode().splitlines()
    my_list = list(map(float, list_proc))
    print(f"Суммарное потребление памяти древа процессов {sum(my_list)}")
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    #pass

if __name__ == "__main__":
    process_count("seriy-pa")
    total_memory_usage(1)
