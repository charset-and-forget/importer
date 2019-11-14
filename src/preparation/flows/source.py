import glob


class SourceFlowBase:
    @classmethod
    def iterate_from_source(cls, source):
        raise NotImplementedError


class FileSourceFlow(SourceFlowBase):
    @classmethod
    def iterate_from_source(cls, source):
        # read files from source mask
        print('Iterating from file source:', source)
        filenames = glob.glob(source)
        for name in filenames:
            print('Iterating from file:', name)
            with open(name, 'rb') as f:
                print('reading from', name)
                content = f.read()
                print('content size:', len(content))
                yield content
