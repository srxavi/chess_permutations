import multiprocessing


def fun(func, q_in, q_out):
    """
    Get a function from the input queue, execute it and put the results in the
    output queue.

    :param func: the function to execute
    :param q_in: the input queue
    :param q_out: the output queue
    """
    while True:
        i, data = q_in.get()
        if i is None:
            break
        result = func(*data)
        q_out.put((i, result))


def parmap(func, iterable, nprocs=multiprocessing.cpu_count(), progress=None):
    """
    An improved version of map from multiprocessing module.
    :param func: the function to execute
    :param iterable: the iterator of the parameters
    :param nprocs: number of concurrent processes
    :param progress: a progress bar
    :return:
    """
    q_in = multiprocessing.Queue()
    q_out = multiprocessing.Queue()
    processes = [multiprocessing.Process(target=fun, args=(func, q_in, q_out))
                 for _ in range(nprocs)]
    for process in processes:
        process.daemon = True
        process.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(iterable)]
    for _ in range(nprocs):
        q_in.put((None, None))
    results = []
    for _ in range(len(sent)):
        results.append(q_out.get())
        if progress:
            progress.update(progress.currval + 1)

    for process in processes:
        process.join()

    return [x for i, x in sorted(results)]
