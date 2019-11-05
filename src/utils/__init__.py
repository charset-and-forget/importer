def chunks(n, source):
    """ Yield successive n-sized chunks from source.
    Example:
        >>> from functools import partial
        >>> chunks3 = partial(chunks, 3)
        >>> chunks3(x for x in xrange(10))
        <generator object chunks at 0x10ac75320>
        >>> [x for x in chunks3(x for x in xrange(10))]
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    source = iter(source)
    while True:
        bunch = []
        for i in xrange(n):
            try:
                bunch.append(next(source))
            except StopIteration:
                if bunch:
                    yield bunch
                raise StopIteration
        yield bunch
