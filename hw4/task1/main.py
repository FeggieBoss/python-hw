from threading       import Thread
from multiprocessing import Process
from time            import time

artifacts_path = f'../artifacts/task1'
kN             = 33
kWorkers       = 10 

def fib(n = kN):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

def measure(calculations):
    # time before calculations
    start = time()

    calculations()

    # time after calculations
    after = time()
    return after - start

def sync_calculations():
    for _ in range(kWorkers):
        fib()

def multithreading_calculations():
    # launching kWorkers threads
    threads = []
    for _ in range(kWorkers):
        t = Thread(target=fib)
        threads.append(t)
        t.start()
    # joining all threads
    for t in threads:
        t.join()

def multiprocessing_calculations():
    # launching kWorkers processes
    processes = []
    for _ in range(kWorkers):
        p = Process(target=fib)
        processes.append(p)
        p.start()
    # joining all processes
    for p in processes:
        p.join()

artifacts_format = """Task: fib({N})
Measuring time of running {K} tasks
Synchronous execution: {sync_t}
Multithreading execution: {threads_t}
Multiprocessing execution {processes_t}
"""

with open(f'{artifacts_path}/artifacts.txt', 'w') as artifacts:
    artifacts.write(artifacts_format.format(
        N = kN, 
        K = kWorkers, 
        sync_t = measure(sync_calculations), 
        threads_t = measure(multithreading_calculations), 
        processes_t = measure(multiprocessing_calculations))
    )
