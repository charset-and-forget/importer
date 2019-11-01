import glob
import json
import os


class FlowBase:
    @classmethod
    def iterate_from_source(cls, source):
        raise NotImplementedError

    @classmethod
    def move_to_destination(cls, response, destination=None):
        raise NotImplementedError


class DumbFlow(FlowBase):
    @classmethod
    def iterate_from_source(cls, source):
        # as is
        for content in source:
            yield content

    @classmethod
    def move_to_destination(cls, response, destination=None):
        if destination is None:
            return response


class FileFlow(FlowBase):
    @classmethod
    def iterate_from_source(cls, source):
        # read files from source mask
        filenames = glob.glob(source)
        for name in filenames:
            with open(name, 'rb') as f:
                print('reading from', name)
                yield f.read()

    @classmethod
    def move_to_destination(cls, response, destination):
        # wrote to separate files in the destination folder
        for key, value in response.items():
            filename = '{}.json'.format(key)
            full_path = os.path.join(destination, filename)
            with open(full_path, 'w') as f:
                json.dump(list(value), f, indent=4)
