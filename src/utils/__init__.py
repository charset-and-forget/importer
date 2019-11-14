def chunks(n, source):
    source = iter(source)
    while True:
        bunch = []
        for i in range(n):
            try:
                bunch.append(next(source))
            except StopIteration:
                if bunch:
                    yield bunch
                return
        yield bunch
