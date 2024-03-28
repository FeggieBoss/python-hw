from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing    import cpu_count
from time               import time
from functools          import partial
import logging 
import math

artifacts_path        = f'../artifacts/task2'
kStepPrecision        = 10000000
kMaxWorkers           = cpu_count() * 2

# Full task
def integrate(f, a, b, n_jobs=1, n_iter=kStepPrecision):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

# generating subtasks
def gen_integrate_subtasks(f, a, b, n_jobs, n_iter=kStepPrecision):
    subtasks = []
    for nth in range(n_jobs):
        # subtask for nth worker
        def subtask(f, a, b, n_jobs, n_iter, nth):
            logging.info(logging_format_start.format(nth=nth))

            acc = 0
            step = (b - a) / n_iter
            sa = a + nth * (b - a) / n_jobs
            for i in range(n_iter // n_jobs):
                acc += f(sa + i * step) * step


            logging.info(logging_format_end.format(nth=nth))
            return acc

        # capturing variables inside subtask
        subtasks.append(partial(subtask, f, a, b, n_jobs, n_iter, nth))

    return subtasks

def measure(calculations, expected):
    # time before calculations
    start = time()

    got = calculations()

    # time after calculations
    after = time()

    # checking that we got correct calculation
    eps = 1e-5
    assert (got - expected) < eps

    return after - start

def calculation_with(tasks, executor):
    futures = []
    for task in tasks:
        f = executor.submit(task)
        futures.append(f)

    sum = 0
    for f in futures:
        sum += f.result()
    return sum


# configuring logging
logger                = logging.getLogger(__name__)
logging_format_header = """Start integration with method=<{executor_name}> and number of workers=<{n_jobs}>"""
logging_format_footer = """End integration with method=<{executor_name}>\n"""
logging_format_start  = """Worker({nth}): start subtask"""
logging_format_end    = """Worker({nth}): end subtask"""
logging.basicConfig(
    filename=f'{artifacts_path}/logs.txt',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# calculating correct answer
args = (math.cos, 0, math.pi / 2)
real_integral = integrate(*args)

artifacts_format = """Task: integrate(f={f}, a={a}, b={b}, n_iter={n_iter})
Measuring time of running {K} tasks
Multithreading execution: {threads_t}
Multiprocessing execution {processes_t}

"""
artifacts_measurements = open(f'{artifacts_path}/artifacts_measurements.txt', 'w')

for n_jobs in range(1, kMaxWorkers+1):
    # generating subtasks of integrate
    subtasks = gen_integrate_subtasks(*args, n_jobs=n_jobs)
    
    # measuring multithreading execution / checking correctness
    thread_executor = ThreadPoolExecutor(max_workers=n_jobs)
    logging.info(logging_format_header.format(executor_name="ThreadPoolExecutor", n_jobs=n_jobs))
    threads_t = measure(partial(calculation_with, subtasks, thread_executor), real_integral)
    logging.info(logging_format_footer.format(executor_name="ThreadPoolExecutor"))

    # measuring multiprocessing execution / checking correctness
    process_executor = ProcessPoolExecutor(max_workers=n_jobs)
    logging.info(logging_format_header.format(executor_name="ProcessPoolExecutor", n_jobs=n_jobs))
    processes_t = measure(partial(calculation_with, subtasks, thread_executor), real_integral)
    logging.info(logging_format_footer.format(executor_name="ProcessPoolExecutor"))

    artifacts_measurements.write(artifacts_format.format(
        f = args[0],
        a = args[1],
        b = args[2],
        K = n_jobs,
        n_iter = kStepPrecision,
        threads_t = threads_t,
        processes_t = processes_t
    ))