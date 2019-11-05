import glob


class SourceFlowBase:
    @classmethod
    def iterate_from_source(cls, source):
        raise NotImplementedError


class FileSourceFlow(SourceFlowBase):
    @classmethod
    def iterate_from_source(cls, source):
        # read files from source mask
        filenames = glob.glob(source)
        for name in filenames:
            with open(name, 'rb') as f:
                print('reading from', name)
                yield f.read()
