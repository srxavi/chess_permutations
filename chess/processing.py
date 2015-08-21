import multiprocessing


def fun(f, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        result = f(*x)
        q_out.put((i, result))


def parmap(func, iterable, nprocs=multiprocessing.cpu_count(), progress=None):
    q_in = multiprocessing.Queue()
    q_out = multiprocessing.Queue()
    processes = [multiprocessing.Process(target=fun, args=(func, q_in, q_out))
                 for _ in range(nprocs)]
    for p in processes:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(iterable)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    results = []
    for _ in range(len(sent)):
        results.append(q_out.get())
        if progress:
            progress.update(progress.currval + 1)

    [p.join() for p in processes]

    return [x for i, x in sorted(results)]
